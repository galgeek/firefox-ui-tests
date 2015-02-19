# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from ..base import BaseLib


class Permissions(BaseLib):
    def remove(self, host, permission):
        with self.marionette.using_context('chrome'):
            self.marionette.execute_script("""
            Cu.import("resource://gre/modules/Services.jsm");
            Services.perms.remove(arguments[0], arguments[1]);
            """, script_args=[host, permission])
