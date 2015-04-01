# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette_driver import Wait
from marionette_driver.errors import NoSuchElementException

from firefox_ui_harness.decorators import skip_if_e10s, skip_under_xvfb
from firefox_ui_harness.testcase import FirefoxTestCase


class TestSSLStatusAfterRestart(FirefoxTestCase):

    def setUp(self):
        FirefoxTestCase.setUp(self)

        self.test_data = [
            {
                'url': 'https://ssl-dv.mozqa.com',
                'identity': '',
                'type': 'verifiedDomain'
            },
            {
                'url': 'https://ssl-ev.mozqa.com/',
                'identity': 'Mozilla Corporation',
                'type': 'verifiedIdentity'
            },
            {
                'url': 'https://ssl-ov.mozqa.com/',
                'identity': '',
                'type': 'verifiedDomain'
            }
        ]

        # Set browser to restore previous session
        self.prefs.set_pref('browser.startup.page', 3)

        self.identity_popup = self.browser.navbar.locationbar.identity_popup

    def tearDown(self):
        try:
            self.identity_popup.close(force=True)
            self.browser.tabbar.close_all_tabs([self.browser.tabbar.tabs[0]])
        except NoSuchElementException:
            # TODO: A NoSuchElementException may be thrown here when the test is skipped
            # as under xvfb.
            pass
        finally:
            FirefoxTestCase.tearDown(self)

    @skip_if_e10s
    @skip_under_xvfb
    # Bug 995801: Test certificate status after browser restart
    def test_ssl_status_after_restart(self):
        for item in self.test_data:
            with self.marionette.using_context('content'):
                self.marionette.navigate(item['url'])
            self.verify_certificate_status(item)
            self.browser.tabbar.open_tab()

        '''
        self.restart()

        i = 0
        for item in self.test_data:
            self.browser.tabbar.tabs[i].switch_to()
            self.verify_certificate_status(item)
            i = i + 1
        '''

    def verify_certificate_status(self, item):
        url, identity, type = item['url'], item['identity'], item['type']

        # Check the favicon
        # TODO: find a better way to check, e.g., mozmill's isDisplayed
        favicon_hidden = self.marionette.execute_script("""
          return arguments[0].hasAttribute("hidden");
        """, script_args=[self.browser.navbar.locationbar.favicon])
        self.assertFalse(favicon_hidden)

        self.identity_popup.box.click()
        Wait(self.marionette).until(lambda _: self.identity_popup.is_open)

        # Check the type shown on the idenity popup doorhanger
        self.assertEqual(self.identity_popup.popup.get_attribute('className'),
                         type,
                         'Extended certificate is verified for ' + url)

        # Check the identity label
        self.assertEqual(self.identity_popup.organization_label.get_attribute('value'),
                         identity,
                         'Identity name is correct for ' + url)

        # Get the information from the certificate
        cert = self.browser.tabbar.selected_tab.certificate

        # Open the Page Info window by clicking the More Information button
        page_info = self.browser.open_page_info_window(
            lambda _: self.identity_popup.more_info_button.click())

        if identity != '':
            owner = cert['organization']
        else:
            owner = page_info.get_property('securityNoOwner')

        try:
            # Verify that the current panel is the security panel
            self.assertEqual(page_info.deck.selected_panel, page_info.deck.security)

            # Verify the domain listed on the security panel
            self.assertIn(self.security.get_domain_from_common_name(cert['commonName']),
                          page_info.deck.security.domain.get_attribute('value'),
                          'Expected domain found in certificate for ' + url)

            # Verify the owner listed on the security panel
            self.assertEqual(page_info.deck.security.owner.get_attribute('value'), owner,
                             'Expected owner label found for ' + url)

            # Verify the verifier listed on the security panel
            self.assertEqual(page_info.deck.security.verifier.get_attribute('value'),
                             cert['issuerOrganization'],
                             'Verifier matches issuer of certificate for ' + url)
        finally:
            page_info.close()
            self.browser.focus()
