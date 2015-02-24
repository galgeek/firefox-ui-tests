# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from marionette import By
from marionette.errors import NoSuchElementException

from firefox_ui_harness.testcase import FirefoxTestCase


class TestSafeBrowsingWarningPages(FirefoxTestCase):

    def setUp(self):
        FirefoxTestCase.setUp(self)

        self.urls = [
            # Phishing URL
            "https://www.itisatrap.org/firefox/its-a-trap.html",
            # Malware URL
            "https://www.itisatrap.org/firefox/its-an-attack.html"
            ]

        self.prefs.set_pref('browser.safebrowsing.enabled', True)
        self.prefs.set_pref('browser.safebrowsing.malware.enabled', True)

        # Give the browser a little time, because SafeBrowsing.jsm takes a
        # while between start up and adding the example urls to the db.
        time.sleep(2)

    def tearDown(self):
        self.perms.remove('www.itisatrap.org', 'safe-browsing')
        self.prefs.restore_all_prefs
        try:
            self.windows.close_all([self.browser])
        finally:
            FirefoxTestCase.tearDown(self)

    def test_warning_pages(self):
        with self.marionette.using_context("content"):
            for unsafe_page in self.urls:
                # Load a test page and test the get me out button
                self.marionette.navigate(unsafe_page)
                self.check_get_me_out_of_here_button(unsafe_page)

                # Load the test page again and test the report button
                self.marionette.navigate(unsafe_page)

                self.check_report_button(unsafe_page)

                # Load the test page again and test the ignore warning button
                self.marionette.navigate(unsafe_page)
                self.check_ignore_warning_button(unsafe_page)

    def check_get_me_out_of_here_button(self, unsafe_page):
        get_me_out_of_here_button = self.marionette.find_element(By.ID, "getMeOutButton")

        # This isn't clickable by the time we get here and needs a delay.
        time.sleep(1)
        get_me_out_of_here_button.click()

        homepage = self.prefs.get_pref('browser.startup.homepage',
                                       interface='nsIPrefLocalizedString')
        self.wait_for_condition(lambda mn: homepage in mn.get_url())

    def check_report_button(self, unsafe_page):
        report_button = self.marionette.find_element(By.ID, "reportButton")

        # This isn't clickable by the time we get here and needs a delay.
        time.sleep(1)
        report_button.click()

        with self.marionette.using_context('chrome'):  # required by execute_script
            if 'its-a-trap' in unsafe_page:
                # mozmill: utils.formatUrlPref("app.support.baseURL") + "phishing-malware"
                # the code commented out below produces this:
                # https://support.mozilla.org/1/firefox/38.0a1/Darwin/en-US/phishing-malware
                # which fails to match the page we're sent to...
                # url = self.marionette.execute_script("""
                #    Cu.import("resource://gre/modules/Services.jsm");
                #    locale = Services.prefs.getCharPref("general.useragent.locale", "");
                #    return (Services.urlFormatter.formatURLPref("app.support.baseURL")
                #                                               + "phishing-malware");
                #    """)
                url = 'https://support.mozilla.org'

            else:
                url = self.marionette.execute_script("""
                   Cu.import("resource://gre/modules/Services.jsm");
                   locale = Services.prefs.getCharPref("general.useragent.locale", "");
                   return (Services.urlFormatter.formatURLPref(
                            "browser.safebrowsing.malware.reportURL") + arguments[0]);
                   """, script_args=[unsafe_page])

        self.wait_for_condition(lambda mn: url in mn.get_url())

    def check_ignore_warning_button(self, unsafe_page):
        ignore_warning_button = self.marionette.find_element(By.ID, "ignoreWarningButton")

        # This isn't clickable by the time we get here and needs a delay.
        time.sleep(1)
        ignore_warning_button.click()

        def find_main_feature_el(mn):
            try:
                mn.find_element("id", "main-feature")
                return True
            except:
                return False

        self.wait_for_condition(find_main_feature_el)
        self.assertRaises(NoSuchElementException, self.marionette.find_element,
                          'id', 'ignoreWarningButton')
        self.assertEquals(self.marionette.get_url(), unsafe_page)
        self.perms.remove('www.itisatrap.org', 'safe-browsing')
