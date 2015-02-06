#!/bin/bash
set -ev

if [ "$TRAVIS_OS_NAME" == "linux" ]; then
    export DISPLAY=:99
    export MOZ_XVFB=1
    /sbin/start-stop-daemon --start --quiet --make-pidfile --pidfile /tmp/custom_xvfb_99.pid \
         --background --exec /usr/bin/Xvfb -- :99 -ac -screen 0 1024x768x24

    sudo apt-get -y update
fi
