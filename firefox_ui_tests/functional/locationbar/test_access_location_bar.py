# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from firefox_ui_harness.decorators import skip_under_xvfb
from firefox_ui_harness.testcase import FirefoxTestCase


class TestAccessLocationBar(FirefoxTestCase):

    def setUp(self):
        FirefoxTestCase.setUp(self)

        # Clear complete history so there's no interference from previous entries.
        self.places.remove_all_history()

        self.test_urls = [
            'layout/mozilla_projects.html',
            'layout/mozilla.html',
            'layout/mozilla_mission.html'
        ]
        self.test_urls = [self.marionette.absolute_url(t)
                          for t in self.test_urls]
        self.test_urls.append('about:blank')

        self.locationbar = self.browser.navbar.locationbar
        self.autocomplete_results = self.locationbar.autocomplete_results
        self.urlbar = self.locationbar.urlbar

    @skip_under_xvfb
    def test_access_locationbar_history(self):

        # Open some local pages, then about:blank
        def load_urls():
            with self.marionette.using_context('content'):
                for url in self.test_urls:
                    self.marionette.navigate(url)
        self.places.wait_for_visited(self.test_urls, load_urls)

        # Need to blur url bar or autocomplete won't load - bug 1038614
        self.marionette.execute_script("""arguments[0].blur();""", script_args=[self.urlbar])

        # Clear contents of url bar to focus, then arrow down for list of visited sites
        # Verify that autocomplete is open and results are displayed
        self.locationbar.clear()
        self.urlbar.send_keys(self.keys.ARROW_DOWN)
        self.wait_for_condition(lambda _: self.autocomplete_results.is_open)
        self.wait_for_condition(lambda _: len(self.autocomplete_results.visible_results) > 1)

        # List of visited sites should appear in this order:
        # layout/mozilla_mission.html
        # layout/mozilla.html
        # layout/mozilla_projects.html

        # Arrow down again to select first item in list
        # Verify first item is selected and selected item populates location bar with url
        self.urlbar.send_keys(self.keys.ARROW_DOWN)
        self.wait_for_condition(lambda _: self.autocomplete_results.selected_index == '0')
        self.assertIn('mozilla_mission', self.locationbar.value)

        # Navigate to the currently selected url
        self.urlbar.send_keys(self.keys.ENTER)

        # Verify that selected url is loaded by verifying the title of the page
        def check_title(mn):
            self.new_page_title = self.marionette.execute_script("""return document.title;""")
            return self.new_page_title == 'Mozilla Mission'
        self.wait_for_condition(check_title)
