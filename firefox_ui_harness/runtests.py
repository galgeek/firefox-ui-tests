# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import copy
import sys

from marionette import BaseMarionetteTestRunner
from marionette.runtests import cli

import firefox_ui_tests

from .arguments import ReleaseTestParser
from .testcase import FirefoxTestCase


class ReleaseTestRunner(BaseMarionetteTestRunner):
    extra_prefs = {
        "browser.tabs.remote.autostart" : False,
        "app.update.auto" : False,
        "app.update.enabled" : False,
        "browser.dom.window.dump.enabled" : True,
        "browser.newtab.url" : "about:blank",
        "browser.newtabpage.enabled" : False,
        "browser.safebrowsing.enabled" : False,
        "browser.safebrowsing.malware.enabled" : False,
        "browser.search.update" : False,
        "browser.sessionstore.resume_from_crash" : False,
        "browser.shell.checkDefaultBrowser" : False,
        "browser.startup.page" : 0,
        "browser.tabs.animate" : False,
        "browser.tabs.warnOnClose" : False,
        "browser.tabs.warnOnOpen" : False,
        "browser.uitour.enabled" : False,
        "browser.warnOnQuit" : False,
        "datareporting.healthreport.service.enabled" : False,
        "datareporting.healthreport.uploadEnabled" : False,
        "datareporting.healthreport.documentServerURI" : "http://%(server)s/healthreport/",
        "datareporting.healthreport.about.reportUrl" : "http://%(server)s/abouthealthreport/",
        "datareporting.policy.dataSubmissionEnabled" : False,
        "datareporting.policy.dataSubmissionPolicyAccepted" : False,
        "dom.ipc.reportProcessHangs" : False,
        "dom.report_all_js_exceptions" : True,
        "extensions.enabledScopes" : 5,
        "extensions.autoDisableScopes" : 10,
        "extensions.getAddons.cache.enabled" : False,
        "extensions.installDistroAddons" : False,
        "extensions.logging.enabled" : True,
        "extensions.showMismatchUI" : False,
        "extensions.update.enabled" : False,
        "extensions.update.notifyUser" : False,
        "geo.provider.testing" : True,
        "javascript.options.showInConsole" : True,
        "security.notification_enable_delay" : 0,
        "signon.rememberSignons" : False,
        "startup.homepage_welcome_url":"about:blank",
        "toolkit.startup.max_resumed_crashes" : -1,
        "toolkit.telemetry.enabled" : False,
    }

    def __init__(self, *args, **kwargs):
        if not kwargs.get('server_root'):
            kwargs['server_root'] = firefox_ui_tests.resources

        prefs = kwargs.get('prefs', {})
        extra_prefs = copy.deepcopy(ReleaseTestRunner.extra_prefs)
        extra_prefs.update(prefs)
        kwargs['prefs'] = extra_prefs

        BaseMarionetteTestRunner.__init__(self, *args, **kwargs)
        self.test_handlers = [FirefoxTestCase]


def run():
    cli(runner_class=ReleaseTestRunner, parser_class=ReleaseTestParser)


if __name__ == '__main__':
    sys.exit(run())
