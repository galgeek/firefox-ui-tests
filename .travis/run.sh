#!/bin/bash
set -e
set -x
if [[ "$(uname -s)" == "Darwin" ]]; then
    firefox-ui-tests --binary /Applications/FirefoxNightly.app/Contents/MacOS/firefox
else
    firefox-ui-tests --binary firefox/firefox
fi
