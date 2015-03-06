# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from marionette_driver import By, expected

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
            self.marionette.navigate(self.url)

            # Get the page's search box and submit button.
            searchbox = self.marionette.find_element(By.ID, 'q')
            button = self.marionette.find_element(By.ID, 'submit')

            # Use the page's search box to submit information.
            searchbox.send_keys(self.test_string)
            button.click()

            # Define a function, per modal dialog unit tests for marionette, to handle warning.
            def alert_present(mn):
                try:
                    Alert(mn).text
                    return True
                except NoAlertPresentException:
                    return False

            # Wait for the warning, check its message text, and "accept" it.
            self.wait_for_condition(lambda _: alert_present(self.marionette))
            warning = Alert(self.marionette)

            # Get the warning message text and replace its two instances of "##" with "\n\n".
            message = self.browser.get_property('formPostSecureToInsecureWarning.message')
            message = message.replace('##', '\n\n')

            # Verify the text matches, then accept the warning
            self.assertEqual(warning.text, message)
            warning.accept()
            self.wait_for_condition(lambda _: not alert_present(self.marionette))

            # Wait while the page updates,
            # then check that search_term contains the expected text.
            self.wait_for_condition(expected.element_stale(searchbox))
            search_term = self.marionette.find_element(By.ID, 'search-term')
            self.assertEqual(search_term.get_attribute('textContent'), self.test_string)
