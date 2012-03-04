#!/bin/bash

export DASHBOARD_HOME='./src/gui/'
export DJANGO_SETTINGS_MODULE=gui.settings
kill -9 `ps -ef | grep "django runserver" | awk 'NR==2{print $2}'`
./bin/python ./src/scripts/stop-services test.service.group

