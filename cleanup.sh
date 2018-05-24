#!/bin/bash

echo GravityBee Clean-up Tool
echo CAUTION: This will delete files from your system.
echo It should only delete files that are created by
echo GravityBee but could delete other important files.

read -n 1 -s -r -p "Press any key to continue"

echo

rm gravitybee-environs*
rm gravitybee-*json
rm gbtestapp-4.2.6*

rm tests/gbtestapp/gravitybee-environs*
rm tests/gbtestapp/gravitybee-*json
rm tests/gbtestapp/gbtestapp-4.2.6*