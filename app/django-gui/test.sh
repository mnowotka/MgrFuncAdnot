#!/bin/bash

cp src/gui/tests/samples/sample_test_01.fasta src/gui/site_media/files/
./bin django testserver src/gui/tests/samples/sample_data.json.zip
