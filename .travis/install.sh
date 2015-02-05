#!/bin/bash

set -ev

if [ "$TRAVIS_OS_NAME" == "linux" ]; then
    sudo apt-get update

    export DISPLAY=:99
    export MOZ_XVFB=1
    /sbin/start-stop-daemon --start --quiet --make-pidfile --pidfile /tmp/custom_xvfb_99.pid \
         --background --exec /usr/bin/Xvfb -- :99 -ac -screen 0 1024x768x24
fi

# As long as we have invasive changes, let's get the trunk version of marionette-client
svn checkout https://github.com/mozilla/gecko-dev/trunk/testing/marionette/client
cd client && sudo python setup.py develop && cd ..

sudo python setup.py develop
sudo pip install mozdownload pep8

# Download Firefox Nightly which is compatible with the Marionette client version used 
mozdownload -t daily

if [ "$TRAVIS_OS_NAME" == "osx" ]; then
    hdiutil mount *firefox*.mac.dmg
    sudo cp -R /Volumes/Nightly/FirefoxNightly.app /Applications
    cd ~
    hdiutil unmount /Volumes/Nightly/
else
    tar -xvf *firefox*.tar.bz2
fi
