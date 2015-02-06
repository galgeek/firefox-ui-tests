#!/bin/bash

set -ev

if [ "$TRAVIS_OS_NAME" == "osx" ]; then
    hdiutil mount *firefox*.mac.dmg
    sudo cp -R /Volumes/Nightly/FirefoxNightly.app /Applications
    cd ~
    hdiutil unmount /Volumes/Nightly/
    export FIREFOX="/Applications/FirefoxNightly.app/Contents/MacOS/firefox"
else
    tar -xvf *firefox*.tar.bz2
    export FIREFOX="firefox/firefox"
fi
