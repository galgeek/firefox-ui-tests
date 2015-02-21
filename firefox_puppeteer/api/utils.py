# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.errors import TimeoutException

from ..base import BaseLib


class Utils(BaseLib):
    """Low-level access to utility actions."""

    def sanitize(self, data_type):
        """Sanitize user data, including cache, cookies, offlineApps, history, formdata,
        downloads, passwords, sessions, siteSettings.

        Usage:
        sanitize():  Clears all user data.
        sanitize({ "sessions": True }): Clears only session user data.

        more: https://dxr.mozilla.org/mozilla-central/source/browser/base/content/sanitize.js

        :param data_type: optional, Information specifying data to be sanitized
        """

        with self.marionette.using_context('chrome'):
            result = self.marionette.execute_async_script("""
              Cu.import("resource://gre/modules/Services.jsm");

              var data_type = arguments[0];

              var data_type = (typeof data_type === "undefined") ? {} : {
                cache: data_type.cache || false,
                cookies: data_type.cookies || false,
                downloads: data_type.downloads || false,
                formdata: data_type.formdata || false,
                history: data_type.history || false,
                offlineApps: data_type.offlineApps || false,
                passwords: data_type.passwords || false,
                sessions: data_type.sessions || false,
                siteSettings: data_type.siteSettings || false
              };

              // Load the sanitize script
              var tempScope = {};
              Cc["@mozilla.org/moz/jssubscript-loader;1"]
              .getService(Ci.mozIJSSubScriptLoader)
              .loadSubScript("chrome://browser/content/sanitize.js", tempScope);

              // Instantiate the Sanitizer
              var s = new tempScope.Sanitizer();
              s.prefDomain = "privacy.cpd.";
              var itemPrefs = Services.prefs.getBranch(s.prefDomain);

              // Apply options for what to sanitize
              for (var pref in data_type) {
                itemPrefs.setBoolPref(pref, data_type[pref]);
              };

              // Sanitize and wait for the promise to resolve
              var finished = false;
              s.sanitize().then(() => {
                for (let pref in data_type) {
                  itemPrefs.clearUserPref(pref);
                };
                marionetteScriptFinished(true);
              }, aError => {
                for (let pref in data_type) {
                  itemPrefs.clearUserPref(pref);
                };
                marionetteScriptFinished(false);
              });
            """, script_args=[data_type])

            if not result:
                raise MarionetteException('Sanitizing of profile data failed.')
