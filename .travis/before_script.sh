#!/bin/bash

set -ev

# Download Firefox Nightly which is compatible with the Marionette client version used 
mozdownload -t daily

if [ "$TRAVIS_OS_NAME" == "osx" ]; then
    hdiutil attach -nobrowse -noautoopen *firefox*.mac.dmg
    cp -R /Volumes/Nightly/FirefoxNightly.app /Applications
    cd ~
    hdiutil unmount /Volumes/Nightly/
else
    tar -xvf *firefox*.tar.bz2
fi
