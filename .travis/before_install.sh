#!/bin/bash
set -ev

if [ "$TRAVIS_OS_NAME" == "linux" ]; then
    /sbin/start-stop-daemon --start --quiet --make-pidfile --pidfile /tmp/custom_xvfb_99.pid \
         --background --exec /usr/bin/Xvfb -- :99 -ac -screen 0 1280x768x24

fi
