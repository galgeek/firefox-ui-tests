#!/bin/bash

set -e
set -x

if [[ "$(uname -s)" == 'Darwin' ]]; then
    DARWIN=true
else
    DARWIN=false
fi

if [[ "$DARWIN" = true ]]; then
    brew update

    # xvfb for OS X?

    # flash via command line for OS X?

else
    sudo apt-get update
    /sbin/start-stop-daemon --start --quiet --make-pidfile --pidfile /tmp/custom_xvfb_99.pid \
         --background --exec /usr/bin/Xvfb -- :99 -ac -screen 0 1024x768x24
    sudo apt-get install flashplugin-nonfree subversion
fi

# As long as we have invasive changes lets get the trunk version of marionette-client
svn checkout https://github.com/mozilla/gecko-dev/trunk/testing/marionette/client
cd client && sudo python setup.py develop && cd ..

sudo python setup.py develop
sudo pip install mozdownload pep8

# Run pep8 on all except the checked out marionette-client folder
pep8 --max-line-length=99 --exclude=client .

# Download Firefox Nightly which is compatible with the Marionette client version used 
mozdownload -t daily

if [[ "$DARWIN" = true ]]; then
    hdiutil mount *firefox*.mac.dmg
    sudo cp -R /Volumes/Nightly/FirefoxNightly.app /Applications
    cd ~
    hdiutil unmount /Volumes/Nightly/
else
    tar -xvf *firefox*.tar.bz2
fi
