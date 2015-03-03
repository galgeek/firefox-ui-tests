# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from marionette_driver import By

from marionette_driver.errors import NoAlertPresentException
from marionette_driver.marionette import Alert

from firefox_ui_harness.testcase import FirefoxTestCase


class TestSubmitUnencryptedInfoWarning(FirefoxTestCase):

    def setUp(self):
        FirefoxTestCase.setUp(self)

        self.url = 'https://ssl-dv.mozqa.com/data/firefox/security/unencryptedsearch.html'
        self.test_string = 'mozilla'

        self.prefs.set_pref('security.warn_submit_insecure', True)

    def test_submit_unencrypted_info_warning(self):
        with self.marionette.using_context('content'):
            # Navigate to the test page.
            self.marionette.navigate(self.url)

            # Get the page's search box and submit button.
            searchbox = self.marionette.find_element(By.ID, 'q')
            button = self.marionette.find_element(By.ID, 'submit')

            # Get the warning message text and replace its two instances of "##" with "\n\n".
            message = self.browser.get_property('formPostSecureToInsecureWarning.message')
            message = message.replace('##', '\n\n')

            # Use the page's search box to submit information.
            searchbox.send_keys(self.test_string)
            button.click()

            # Define a function, from marionette client unit tests, to help handle warning.
            def alert_present(self):
                try:
                    Alert(self.marionette).text
                    return True
                except NoAlertPresentException:
                    return False

            # Wait for the warning, check its message text, and "accept" it.
            self.wait_for_condition(lambda _: alert_present(self))
            self.assertEqual(Alert(self.marionette).text, message)
            Alert(self.marionette).accept()
            self.wait_for_condition(lambda _: not alert_present(self))

            # Wait while the search results page (re)loads,
            # then check that search_term contains the expected text.
            time.sleep(1)
            search_term = self.marionette.find_element(By.ID, 'search-term')
            self.assertEqual(search_term.get_attribute('textContent'), self.test_string)
