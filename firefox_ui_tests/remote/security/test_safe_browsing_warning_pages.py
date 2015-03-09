# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from marionette_driver import By, expected

from firefox_ui_harness.testcase import FirefoxTestCase


class TestSafeBrowsingWarningPages(FirefoxTestCase):

    def setUp(self):
        FirefoxTestCase.setUp(self)

        self.urls = [
            # Phishing URL
            'https://www.itisatrap.org/firefox/its-a-trap.html',
            # Malware URL
            'https://www.itisatrap.org/firefox/its-an-attack.html'
            ]

        self.prefs.set_pref('browser.safebrowsing.enabled', True)
        self.prefs.set_pref('browser.safebrowsing.malware.enabled', True)

        # Give the browser a little time, because SafeBrowsing.jsm takes a
        # while between start up and adding the example urls to the db.
        # hg.mozilla.org/mozilla-central/file/46aebcd9481e/browser/base/content/browser.js#l1194
        time.sleep(3)

    def tearDown(self):
        try:
            self.utils.remove_perms('www.itisatrap.org', 'safe-browsing')
        finally:
            FirefoxTestCase.tearDown(self)

    def test_warning_pages(self):
        with self.marionette.using_context("content"):
            for unsafe_page in self.urls:
                # Load a test page, then test the get me out button
                self.marionette.navigate(unsafe_page)
                # Wait for the DOM to receive events for about:blocked
                time.sleep(1)
                self.check_get_me_out_of_here_button(unsafe_page)

                # Load the test page again, then test the report button
                self.marionette.navigate(unsafe_page)
                # Wait for the DOM to receive events for about:blocked
                time.sleep(1)
                self.check_report_button(unsafe_page)

                # Load the test page again, then test the ignore warning button
                self.marionette.navigate(unsafe_page)
                # Wait for the DOM to receive events for about:blocked
                time.sleep(1)
                self.check_ignore_warning_button(unsafe_page)

    def check_get_me_out_of_here_button(self, unsafe_page):
        button = self.marionette.find_element(By.ID, "getMeOutButton")
        button.click()

        self.wait_for_condition(lambda mn: self.browser.default_homepage in mn.get_url())

    def check_report_button(self, unsafe_page):
        button = self.marionette.find_element(By.ID, "reportButton")
        button.click()

        # Wait for the button to become stale, then wait for page load
        # so we can verify the url
        self.wait_for_condition(expected.element_stale(button))
        # TODO: Bug 1140470: use replacement for mozmill's waitforPageLoad
        self.wait_for_condition(lambda mn: mn.execute_script("""
          return document.readyState == 'complete';
        """))

        # Get the base URL to check; this will result in a redirect.
        with self.marionette.using_context('chrome'):
            if 'its-a-trap' in unsafe_page:
                url = self.marionette.execute_script("""
                  Components.utils.import("resource://gre/modules/Services.jsm");
                  return Services.urlFormatter.formatURLPref("app.support.baseURL")
                                                             + "phishing-malware";
                """)
            else:
                url = self.marionette.execute_script("""
                  Components.utils.import("resource://gre/modules/Services.jsm");
                  return Services.urlFormatter.formatURLPref(
                  "browser.safebrowsing.malware.reportURL") + arguments[0];
                """, script_args=[unsafe_page])

        # check that our current url matches the final url we expect
        self.assertEquals(self.marionette.get_url(), self.browser.get_final_url(url))

    def check_ignore_warning_button(self, unsafe_page):
        button = self.marionette.find_element(By.ID, 'ignoreWarningButton')
        button.click()

        self.wait_for_condition(expected.element_stale(button))
        self.wait_for_condition(expected.element_present(By.ID, 'main-feature'))
        self.assertEquals(self.marionette.get_url(), self.browser.get_final_url(unsafe_page))

        # Clean up by removing safe browsing permission for unsafe page
        self.utils.remove_perms('www.itisatrap.org', 'safe-browsing')
