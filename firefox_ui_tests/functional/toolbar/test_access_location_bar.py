# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette import By

from firefox_puppeteer.api.keys import Keys
from firefox_puppeteer.ui.windows import BrowserWindow
from firefox_ui_harness.decorators import skip_under_xvfb
from firefox_ui_harness.testcase import FirefoxTestCase


class TestAccessLocationBar(FirefoxTestCase):

    def setUp(self):
        FirefoxTestCase.setUp(self)

        # To prepare for tests, open new browser window,
        self.browser.open_window()
        self.location_bar = self.browser.navbar.locationbar
        self.url_bar = self.location_bar.urlbar

        # Purge history
        self.marionette.execute_script("""
            let count = gBrowser.sessionHistory.count;
            gBrowser.sessionHistory.PurgeHistory(count);
        """)

        # Navigate to several urls in order to populate history
        self.test_urls = [
            'layout/mozilla_projects.html',
            'layout/mozilla_mission.html',
            'layout/mozilla.html']
        self.test_urls = [self.marionette.absolute_url(t)
                          for t in self.test_urls]

        for url in self.test_urls:
            self.location_bar.load_url(url)

        with self.marionette.using_context('content'):
            self.marionette.navigate('about:blank')

    @skip_under_xvfb
    def test_access_location_bar_history(self):
        # Need to blur url bar or autocomplete won't load - bug 1038614
        self.marionette.execute_script("arguments[0].blur();", script_args=[self.url_bar])

        # Clear contents of url bar to focus
        self.location_bar.clear()

        # Arrow down to navigate list of visited sites
        self.url_bar.send_keys(Keys.ARROW_DOWN)

        # Verify that autocomplete is open
        def auto_complete_open(mn):
            return self.location_bar.autocomplete_results.is_open
        self.wait_for_condition(auto_complete_open)

        # Verify that results are displayed in autocomplete
        def auto_complete_results(mn):
            self.location_bar_value_before = self.location_bar.value
            return len(self.location_bar.autocomplete_results.visible_results) > 1
        self.wait_for_condition(auto_complete_results)

        # Arrow down again to select first item in list
        self.url_bar.send_keys(Keys.ARROW_DOWN)

        # Verify that first item in list is selected
        def auto_complete_selected_item(mn):
            self.results = self.location_bar.autocomplete_results.results
            return self.results.get_attribute('selectedIndex') == '0'
        self.wait_for_condition(auto_complete_selected_item)

        # Verify that selected item populates location bar with url
        def check_url_from_selection(mn):
            self.page_title_before = self.marionette.execute_script("return document.title;")
            return self.location_bar.value != self.location_bar_value_before
        self.wait_for_condition(check_url_from_selection)
        self.url_bar.send_keys(Keys.ENTER)

        # Verify that selected url is loaded by verifying the title of the page has changed
        def check_title(mn):
            self.new_page_title = self.marionette.execute_script("return document.title;")
            return self.new_page_title != self.page_title_before
        self.wait_for_condition(check_title)
        self.windows.close_all(self.browser)