#!/bin/bash

export DASHBOARD_HOME='./src/gui/'
export DJANGO_SETTINGS_MODULE=gui.settings
rm -f src/gui/var/lock/.s.dashboard.test.service.group.lock
./bin/python ./src/scripts/start-services test.service.group
./bin/django runserver  > /dev/null 2>&1 &
