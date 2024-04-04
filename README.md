# DelhiMetroNavigation

This project is being developed to do functional automation testing on Delhi Metro Navigation application.

It consists of following directories:

1. /Apk - It contains apk of the application
2. /images - It contains images which are needed to write the test script
3. /recording - It contains recording of the test suite issue replication
4. /report - It contains allure report
5. /tests - It contains actual test suite which needs to be executed
6. /utilities - It contains generic functions and paths which are needed throughout the project

To run the test suite, following needs to be installed on the system : 

  1. Python
  2. Appium Server
  3. Pytest by using 'pip install pytest'
  4. Appium-Python-Client by using 'pip install Appium-Python-Client'
  5. Airtest by using 'pip install airtest'
  6. Android SDK
  7. iOS Dependencies:
      Xcode
      Carthage by using 'brew install carthage'
      ideviceinstaller by using 'brew install ideviceinstaller'

Command to execute the test suite from root directory: 

pytest tests/testMetro.py --alluredir=report

Command to check the report :

allure serve report 
