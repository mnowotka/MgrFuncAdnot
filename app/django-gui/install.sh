#!/bin/bash

python bootstrap.py
./bin/buildout
./bin/django syncdb --noinput
./bin/django collectstatic --noinput
