#!/bin/bash

export DASHBOARD_HOME='./src/gui/'
export DJANGO_SETTINGS_MODULE=gui.settings
./bin/django runserver  > /dev/null 2>&1 &
sleep 1
rm -f src/gui/var/lock/.s.dashboard.test.service.group.lock
./bin/python ./src/scripts/start-services test.service.group

