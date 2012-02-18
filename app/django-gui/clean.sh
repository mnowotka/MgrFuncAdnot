#!/bin/bash

./stopdb.sh
git clean -fX
rm -rf bin
rm -rf develop-eggs
rm -rf downloads
rm -rf eggs
rm -rf parts
rm -rf src/django_gui.egg-info

