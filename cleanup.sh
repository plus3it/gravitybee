#!/bin/bash

echo GravityBee Clean-up Tool
echo CAUTION: This will delete files from your system.
echo It should only delete files that are created by
echo GravityBee but could delete other important files.

read -n 1 -s -r -p "Press any key to continue"

echo

rm -rf .gravitybee
rm -rf .pytest_cache

rm -rf gravitybee/__pycache__

rm -rf tests/__pycache__
rm -rf tests/gbtestapp/src/gbtestapp/__pycache__
rm -rf tests/gbtestapp/src/gbtestapp/gbextradata/__pycache__
rm -rf tests/gbtestapp/.pytest_cache
rm -rf tests/gbtestapp/src/gbtestapp.egg-info

rm -rf gbtestapp-4.2.6*

rm -rf gravitybee.egg-info

rm -rf tests/gbtestapp/.gravitybee
