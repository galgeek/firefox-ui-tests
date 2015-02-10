# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette import By

from firefox_ui_harness.decorators import skip_under_xvfb
from firefox_ui_harness.testcase import FirefoxTestCase


class TestAccessLocationBar(FirefoxTestCase):

    def setUp(self):
        FirefoxTestCase.setUp(self)
        self.location_bar = self.browser.navbar.locationbar
        self.url_bar = self.location_bar.urlbar


    @skip_under_xvfb
    def test_access_location_bar_history(self):
        # Purge history
        self.places.remove_all_history()

        # Navigate to several urls in order to populate history
        self.test_urls = [
            'layout/mozilla_projects.html',
            'layout/mozilla.html',
            'layout/mozilla_mission.html']
        self.test_urls = [self.marionette.absolute_url(t)
                          for t in self.test_urls]

        for url in self.test_urls:
            self.location_bar.load_url(url)

        with self.marionette.using_context('content'):
            self.marionette.navigate('about:blank')
        # Need to blur url bar or autocomplete won't load - bug 1038614
        self.marionette.execute_script("""arguments[0].blur();""", script_args=[self.url_bar])

        # Clear contents of url bar to focus
        self.location_bar.clear()

        # Arrow down to navigate list of visited sites.
        # They should appear in this order:
        # layout/mozilla_mission.html
        # layout/mozilla.html
        # layout/mozilla_projects.html
        self.url_bar.send_keys(self.keys.ARROW_DOWN)

        # Verify that autocomplete is open
        self.wait_for_condition(lambda _: self.location_bar.autocomplete_results.is_open)

        # Verify that results are displayed in autocomplete
        self.wait_for_condition(lambda _: len(self.location_bar.autocomplete_results.visible_results) > 1)

        # Arrow down again to select first item in list
        self.url_bar.send_keys(self.keys.ARROW_DOWN)

        # Verify that first item in list is selected
        def auto_complete_selected_item(mn):
            # TODO: update to 'visible_results' when 'selected_index' property exists
            self.results = self.location_bar.autocomplete_results.results 
            return self.results.get_attribute('selectedIndex') == '0'
        self.wait_for_condition(auto_complete_selected_item)

        # Verify that selected item populates location bar with url
        self.assertEqual(self.location_bar.value, self.marionette.absolute_url('layout/mozilla_mission.html'))

        # Navigate to the currently selected url
        self.url_bar.send_keys(self.keys.ENTER)

        # Verify that selected url is loaded by verifying the title of the page
        def check_title(mn):
            self.new_page_title = self.marionette.execute_script("""return document.title;""")
            return self.new_page_title == 'Mozilla Mission'
        self.wait_for_condition(check_title)
