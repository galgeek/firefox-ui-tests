# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette_driver import By, Wait

from firefox_puppeteer.testcases import FirefoxTestCase


class TestOpenInBackground(FirefoxTestCase):

    def setUp(self):
        FirefoxTestCase.setUp(self)

        self.browser.tabbar.close_all_tabs([self.browser.tabbar.tabs[0]])
        self.prefs.set_pref("browser.tabs.loadInBackground", True)

        self.test_url = self.marionette.absolute_url('tabbedbrowsing/openinnewtab.html')

    def tearDown(self):
        try:
            self.browser.tabbar.close_all_tabs([self.browser.tabbar.tabs[0]])
        finally:
            FirefoxTestCase.tearDown(self)

    def test_open_in_background(self):
        tabbar = self.browser.tabbar
        self.browser.navbar.locationbar.load_url(self.test_url)
        with self.marionette.using_context('content'):
            Wait(self.marionette).until(lambda mn: mn.get_url() == self.test_url)

            self.assertEqual(len(tabbar.tabs), 1)
            self.assertEqual(tabbar.selected_index, 0)

            link = self.marionette.find_element(By.NAME, 'link_1')
            link.context_click()
            # js: var contextMenuItem = this.getElement({type: "openLinkInNewTab"}); ???
            context_menu_item = self.marionette.find_element(By.ID, 'openLinkInNewTab')
            context_menu_item.click()

            self.assertEqual(len(tabbar.tabs), 2)
            # if we opened sucessfully in background, we should still be on 1st tab
            self.assertEqual(tabbar.tabs[0].handle, self.marionette.current_window_handle)
            tabbar.switch_to(1)
            self.assertEqual(tabbar.tabs[1].handle, self.marionette.current_window_handle)
            tabbar.switch_to(0)
            self.assertEqual(tabbar.tabs[0].handle, self.marionette.current_window_handle)

            link = self.marionette.find_element(By.NAME, 'link_2')
            link.context_click()
            # js: var contextMenuItem = this.getElement({type: "openLinkInNewTab"}); ???
            context_menu_item = self.marionette.find_element(By.ID, 'openLinkInNewTab')
            context_menu_item.click()
        
            link = self.marionette.find_element(By.NAME, 'link_3')
            link.context_click()
            # js: var contextMenuItem = this.getElement({type: "openLinkInNewTab"});
            context_menu_item = self.marionette.find_element(By.ID, 'openLinkInNewTab')
            context_menu_item.click()

            self.assertEqual(len(tabbar.tabs), 4)

            tabbar.switch_to(1)
            Wait(self.marionette).until(expected.element_present(lambda m:
                                        m.find_element(By.ID, '1')))
            tabbar.switch_to(2)
            Wait(self.marionette).until(expected.element_present(lambda m:
                                        m.find_element(By.ID, '2')))
            tabbar.switch_to(3)
            Wait(self.marionette).until(expected.element_present(lambda m:
                                        m.find_element(By.ID, '3')))

            self.browser.tabbar.close_all_tabs([self.browser.tabbar.tabs[0]])