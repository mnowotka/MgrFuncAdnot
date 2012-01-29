#!/bin/bash

python bootstrap.py
./bin/buildout
./bin/django syncdb
./bin/django collectstatic
