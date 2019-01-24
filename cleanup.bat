@echo off
echo GravityBee Clean-up Tool
echo CAUTION: This will delete files from your system.
echo It should only delete files that are created by
echo GravityBee but could delete other important files.

pause

@rd /q /s .gravitybee
@rd /q /s .pytest_cache

@rd /q /s gravitybee\__pycache__

@rd /q /s tests\__pycache__
@rd /q /s tests\gbtestapp\src\gbtestapp\__pycache__
@rd /q /s tests\gbtestapp\src\gbtestapp\gbextradata\__pycache__
@rd /q /s tests\gbtestapp\.pytest_cache
@rd /q /s tests\gbtestapp\src\gbtestapp.egg-info

del /q /s /f gbtestapp-4.2.6*

@rd /q /s gravitybee.egg-info

@rd /q /s tests\gbtestapp\.gravitybee
