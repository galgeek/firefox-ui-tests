# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette_driver.errors import NoSuchElementException

from firefox_ui_harness.decorators import skip_under_xvfb
from firefox_ui_harness.testcase import FirefoxTestCase


class TestSecurityInfoViaMoreInformation(FirefoxTestCase):

    def setUp(self):
        FirefoxTestCase.setUp(self)

        self.url = 'https://ssl-ev.mozqa.com/'

        self.identity_popup = self.browser.navbar.locationbar.identity_popup

    def tearDown(self):
        try:
            self.identity_popup.close(force=True)
            self.windows.close_all([self.browser])
        except NoSuchElementException:
            # TODO: A NoSuchElementException may be thrown here when the test is skipped
            # as under xvfb.
            pass
        finally:
            FirefoxTestCase.tearDown(self)

    @skip_under_xvfb
    def test_security_info_via_more_information(self):
        with self.marionette.using_context('content'):
            self.marionette.navigate(self.url)

        # Get the information from the certificate
        cert = self.browser.tabbar.selected_tab.certificate

        self.identity_popup.box.click()
        self.wait_for_condition(lambda _: self.identity_popup.is_open)

        # Open the Page Info window by clicking the More Information button
        page_info = self.browser.open_page_info_window(
            lambda _: self.identity_popup.more_info_button.click())

        try:
            # TODO: Bug 1144493 workaround to make sure Page Info's security tab is selected
            page_info.deck.select(page_info.deck.security)

            # Verify that the current panel is the security panel
            self.assertEqual(page_info.deck.selected_panel, page_info.deck.security)

            # Verify the domain listed on the security panel
            self.assertIn(cert['commonName'],
                          page_info.deck.security.domain.get_attribute('value'))

            # Verify the owner listed on the security panel
            self.assertEqual(page_info.deck.security.owner.get_attribute('value'),
                             cert['organization'])

            # Verify the verifier listed on the security panel
            self.assertEqual(page_info.deck.security.verifier.get_attribute('value'),
                             cert['issuerOrganization'])

            page_info.close()
        finally:
            self.browser.focus()
