# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from firefox_ui_harness.decorators import skip_under_xvfb
from firefox_ui_harness.testcase import FirefoxTestCase


class TestEscapeAutocomplete(FirefoxTestCase):

    def tearDown(self):
        autocompleteresults = self.browser.navbar.locationbar.autocomplete_results

        if autocompleteresults.is_open:
            autocompleteresults.close(force=True)
            self.wait_for_condition(not autocompleteresults.is_open)

        FirefoxTestCase.tearDown(self)

    @skip_under_xvfb
    def test_escape_autocomplete(self):
        # Clear complete history so there's no interference from previous entries.
        self.places.remove_all_history()

        # Open some local pages to set up the test environment.
        self.test_urls = [
            'layout/mozilla.html',
            'layout/mozilla_community.html',
        ]
        self.test_urls = [self.marionette.absolute_url(t)
                          for t in self.test_urls]

        def load_urls():
            with self.marionette.using_context('content'):
                for url in self.test_urls:
                    self.marionette.navigate(url)
        self.places.wait_for_visited(self.test_urls, load_urls)

        # Set variables
        TEST_STRING = 'mozilla'

        locationbar = self.browser.navbar.locationbar
        autocompleteresults = locationbar.autocomplete_results

        # Clear the location bar, type the test string, check that autocomplete list opens
        locationbar.clear()
        locationbar.urlbar.send_keys(TEST_STRING)
        self.assertEqual(locationbar.value, TEST_STRING)
        self.wait_for_condition(lambda _: autocompleteresults.is_open)

        # Press escape, check location bar value, check autocomplete list closed
        locationbar.urlbar.send_keys(self.keys.ESCAPE)
        self.assertEqual(locationbar.value, TEST_STRING)
        self.assertFalse(autocompleteresults.is_open)

        # Press escape again and check that locationbar returns to the page url
        locationbar.urlbar.send_keys(self.keys.ESCAPE)
        self.assertEqual(locationbar.value, self.test_urls[-1])
