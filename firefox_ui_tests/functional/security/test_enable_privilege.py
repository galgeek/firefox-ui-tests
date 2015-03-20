# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette_driver import By

from firefox_ui_harness.testcase import FirefoxTestCase


class TestEnablePrivilege(FirefoxTestCase):

    def setUp(self):
        FirefoxTestCase.setUp(self)

        self.url = self.marionette.absolute_url('security/enable_privilege.html')

        #self.prefs.set_pref(
        #    'security.turn_off_all_security_so_that_viruses_can_take_over_this_computer', False)

    def test_enable_privilege(self):
        with self.marionette.using_context('content'):
            self.marionette.navigate(self.url)

            result = self.marionette.find_element(By.ID, 'result')
            self.assertEqual(result.get_attribute('textContent'), 'PASS')
