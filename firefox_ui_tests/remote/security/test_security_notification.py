# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from marionette import By
from marionette.errors import MarionetteException

from firefox_ui_harness.testcase import FirefoxTestCase


class TestSecurityNotification(FirefoxTestCase):

    def setUp(self):
        FirefoxTestCase.setUp(self)

        self.test_data = [
            # Invalid cert page
            'https://summitbook.mozilla.org',
            # Secure page
            'https://ssl-ev.mozqa.com/',
            # Unsecure page
            'http://www.mozqa.com'
        ]

        self.identity_box = self.browser.navbar.locationbar.identity_popup.box

    def tearDown(self):
        try:
            self.windows.close_all([self.browser])
        finally:
            FirefoxTestCase.tearDown(self)

    def test_security_notification(self):

        # Go to a secure (https) site
        with self.marionette.using_context('content'):
            self.marionette.navigate(self.test_data[1])

        self.wait_for_condition(lambda _: self.identity_box.get_attribute('className') ==
                                'verifiedIdentity')

        # Go to an insecure (http) site
        with self.marionette.using_context('content'):
            self.marionette.navigate(self.test_data[2])

        self.wait_for_condition(lambda _: self.identity_box.get_attribute('className') ==
                                'unknownIdentity')

        self.marionette.set_context('content')

        # Go to a site that has an invalid (expired) cert
        self.assertRaises(MarionetteException, self.marionette.navigate, self.test_data[0])

        # Wait for about:error page
        time.sleep(1)

        # Verify the text in Technical Content contains the page with invalid cert
        text = (self.marionette.find_element(By.ID, 'technicalContentText')).get_attribute(
            'textContent')
        self.assertTrue(self.test_data[0][8:] in text)

        # Verify the "Get Me Out Of Here!" and "Add Exception" buttons appear
        self.assertIsNotNone(self.marionette.find_element(By.ID, 'getMeOutOfHereButton'))
        self.assertIsNotNone(self.marionette.find_element(By.ID, 'exceptionDialogButton'))

        # Verify the error code is correct
        self.assertTrue('sec_error_expired_certificate' in text)
