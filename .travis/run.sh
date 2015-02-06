#!/bin/bash

set -ev

if [ "$TRAVIS_OS_NAME" == "osx" ]; then
    firefox-ui-tests --binary /Applications/FirefoxNightly.app/Contents/MacOS/firefox
else
    firefox-ui-tests --binary firefox/firefox
fi
