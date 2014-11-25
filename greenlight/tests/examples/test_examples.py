# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from greenlight.harness.testcase import FirefoxTestCase

class TestExampleOne(FirefoxTestCase):
    """This is a test class containing stubs of example tests designed to
    demonstrate fundamentals of marionette based tests and the Firefox Puppeteer
    libraries.
    """

    def setUp(self):
        # Set up runs before every test method.
        FirefoxTestCase.setUp(self)


    def tearDown(self):
        # Tear down runs after every test method.
        # Anything about the browser that's changed in a test should be
        # reverted to its original state either in a test method or in
        # tearDown.
        FirefoxTestCase.tearDown(self)

    # Each test method should be small, and cover a single feature or unit of
    # specification.
    def test_back_forward(self):
        # Test spec:
        # Clicking the back button followed by the forward button in a tab with history
        # should navigate to pages reflecting the actual browsing history.

        # Navigation can be synthesized with self.client.navigate(<url>), and the url of
        # the current page can be accessed from self.client.get_url.

        # The navbar library (http://firefox-puppeteer.readthedocs.org/en/latest/ui/navbar.html)
        # has definitions for the back and forward buttons.

        # Keep in mind that navigate and get_url should be used from content scope, while
        # calling into the navbar and interacting with elements returned from it requires
        # chrome scope. To switch between scopes, use self.client.set_context('chrome')
        # or self.client.set_context('content'), or use a with block:
        # with self.client.using_context('chrome'):
        #     # Code running in chrome scope
        # # Code running in original scope
        pass


    def test_new_tab(self):
        # Test spec:
        # Clicking the new_tab button should result in a new tab being opened.

        # The tabs library (http://firefox-puppeteer.readthedocs.org/en/latest/ui/tabbar.html)
        # can be accessed from this method as self.browser.tabbar, and has everything needed for
        # this test.

        # Roughly, this test should use a puppeteer library to open a new tab,
        # assert that a new tab has been opened, and then close that tab to return the
        # browser to the state it held at the beginning of the test.
        pass


    def test_new_tab_pref(self):
        # Test spec:
        # Setting the browser.newtab.url pref should set the url of a newly opened
        # tab.

        # The prefs library (http://firefox-puppeteer.readthedocs.org/en/latest/api/prefs.html)
        # has most of what's needed for this test beyond test_new_tab.
        # Use self.browser.navbar.location to verify the destination url, and close the tab and
        # restore the pref after doing so.
        pass
