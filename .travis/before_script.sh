#!/bin/bash

set -ev

# Download Firefox Nightly which is compatible with the Marionette client version used 
mozdownload -t daily

if [ "$TRAVIS_OS_NAME" == "osx" ]; then
    # hdiutil mount *firefox*.mac.dmg - works!
    #from http://mxr.mozilla.org/comm-central/source/mozilla/testing/mozbase/mozinstall/mozinstall/mozinstall.py#240 ...
    hdiutil attach -nobrowse -noautoopen *firefox*.mac.dmg
    cp -R /Volumes/Nightly/FirefoxNightly.app /Applications
    cd ~
    hdiutil unmount /Volumes/Nightly/
    env BINARY=/Applications/FirefoxNightly.app/Contents/MacOS/firefox
else
    tar -xvf *firefox*.tar.bz2
    env BINARY=firefox/firefox
fi
