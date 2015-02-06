#!/bin/bash
set -ev

if [ "$TRAVIS_OS_NAME" == "linux" ]; then
    env DISPLAY=:99
    env MOZ_XVFB=1
    /sbin/start-stop-daemon --start --quiet --make-pidfile --pidfile /tmp/custom_xvfb_99.pid \
         --background --exec /usr/bin/Xvfb -- :99 -ac -screen 0 1024x768x24

    sudo apt-get update -qq
    sudo apt-get install python-pip python-virtualenv
    # sudo -H pip install --upgrade pip
    # sudo -H pip install virtualenv
fi
