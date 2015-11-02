#!/bin/bash
set -ev

if [[ $LOCALE = 'en-US' ]]
then
    mozdownload --type daily --branch mozilla-central
else
    mozdownload --type daily --branch mozilla-aurora --locale ta
fi
