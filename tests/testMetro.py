import random
import subprocess
from appium import webdriver
import os, sys, pytest, allure, time
from allure import attachment_type
from airtest.core.api import *
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
# So that we can run this file from anywhere
workingDir =os.path.dirname(os.path.dirname(__file__))
sys.path.append(workingDir)
from utilities.pathUtil import *
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from appium.options.android import UiAutomator2Options
from appium.options.ios import xcuitest
deviceRef = connect_device("Android:" + 'emulator-5554')

desired_caps = {
    # For Android 
    'platformName' : 'Android',
    'deviceName' : 'emulator-5554'
    # For iOS
   ''' platform ='iOS'
    deviceid = '192.168.5.60' '''
}

options = UiAutomator2Options().load_capabilities(desired_caps)
# For iOS
# options = xcuitest().load_capabilities(desired_caps)

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub',options=options)

wait = WebDriverWait(driver, timeout=60,ignored_exceptions=[NoSuchElementException])

# TC-1 : To test whether the application is installed or not on the device 
# If application not installed then, install the same 
@allure.description("Check whether the application is installed or not.\n If not then, install the same")
def test_app():
    deviceRef.start_recording(orientation=2,mode="ffmpeg",max_time=3600,output="recording/metro.mp4")
    is_app_installed = driver.is_app_installed(packageName)
    if not is_app_installed:
        print("apk is not installed on the device. \nNow installing the same ...")
        path = "./Apk/delhimetronavigator.apk"
        # For Android
        subprocess.run(f"adb -s emulator-5554 install {path}", shell=True) # installing the app
        # For iOS
        # subprocess.run(f"ideviceinstaller -u 192.168.5.60 -i {path}", shell=True)
        time.sleep(60)
    else:
        print("apk is already installed on the device")
    driver.activate_app(packageName) 
    assert wait.until(EC.presence_of_element_located((AppiumBy.XPATH,fetchXPath(desired_caps["platformName"],"Delhi Metro Navigator"))))
    assert exists(Template("./images/RemoveAds.png"))
    allure.attach(driver.get_screenshot_as_png(),name="AppLobby",attachment_type=attachment_type.PNG)
    print("Lobby successfully launched")


# TC-2 : It tests the Remove Ads tab 
@allure.description("It checks the functionality of Remove Ads tab")
def test_RemoveAds():
    AdsEle = wait.until(EC.presence_of_element_located((AppiumBy.XPATH,fetchXPath(desired_caps["platformName"],"Remove Ads"))))
    AdsEle.click()
    assert exists(Template("./images/RemoveAds.png")) # 
    print("Remove Ads tab found successfully")
    allure.attach(driver.get_screenshot_as_png(),name="Remove Ads",attachment_type=attachment_type.PNG)
    

# TC-3 : It tests the fare tab and its functionality
@allure.description("It checks the fucntionality of Fare tab and show the fare price")
def test_Fare():
    FareEle = wait.until(EC.presence_of_element_located((AppiumBy.XPATH,fetchXPath(desired_caps["platformName"],"Fare"))))
    FareEle.click()
    assert wait.until(EC.presence_of_element_located((AppiumBy.XPATH,fetchXPath(desired_caps["platformName"],"Show Fare"))))
    assert exists(Template("./images/ShowFare.png"))
    print("Fare tab loads successfully")
    SearchSrc = wait.until(EC.presence_of_element_located((AppiumBy.ID,path["FareSource"])))
    SearchSrc.click()
    SearchSrc = wait.until(EC.presence_of_element_located((AppiumBy.ID,path["EditText"])))
    src_key = MetroStations[random.randint(1,40)]
    SearchSrc.send_keys(f"{src_key}")
    time.sleep(2)
    Ele = wait.until(EC.presence_of_element_located((AppiumBy.ID,path["clickStation"])))
    Ele.click()
    SearchDst = wait.until(EC.presence_of_element_located((AppiumBy.ID,path["FareDestination"])))
    SearchDst.click()
    SearchDst = wait.until(EC.presence_of_element_located((AppiumBy.ID,path["EditText"])))
    dst_key = MetroStations[random.randint(1,40)]
    SearchDst.send_keys(f"{dst_key}")
    Ele = wait.until(EC.presence_of_element_located((AppiumBy.ID,path["clickStation"])))
    Ele.click()
    ShowFare = wait.until(EC.presence_of_element_located((AppiumBy.XPATH,fetchXPath(desired_caps["platformName"],"Show Fare"))))
    ShowFare.click()
    farePrice = wait.until(EC.presence_of_element_located((AppiumBy.ID,path["farePrice"]))).text
    print(f"Total Fare from {src_key} to {dst_key} is : {farePrice}")
    allure.attach(driver.get_screenshot_as_png(),name="Fare",attachment_type=attachment_type.PNG)
    driver.back()


# TC-4 : It tests whether map is visible or not
@allure.description("To verify whether map is visible to the user or not")
def test_Map():
    MapEle = wait.until(EC.presence_of_element_located((AppiumBy.XPATH,fetchXPath(desired_caps["platformName"],"Map"))))
    MapEle.click()
    # Searching whether map is visible on the screen
    assert wait.until(EC.presence_of_element_located((AppiumBy.XPATH,fetchXPath(desired_caps["platformName"],"Map"))))
    assert exists(Template("./images/MapImage.png"))
    print("Map loads successfully")
    allure.attach(driver.get_screenshot_as_png(),name="Map",attachment_type=attachment_type.PNG)
    driver.back()


# TC-5 : It checks the functionality of Route tab
@allure.description("To verify the functionality of Route tab")
def test_Route():
    # changes
    Srcmetro = MetroStations[random.randint(1,40)]
    Dstmetro = MetroStations[random.randint(1,40)]
    RouteEle = wait.until(EC.presence_of_element_located((AppiumBy.XPATH,fetchXPath(desired_caps["platformName"],"Route"))))
    RouteEle.click()
    # set Source
    StartpathElement = wait.until(EC.presence_of_element_located((AppiumBy.ID,path["RouteSource"])))
    StartpathElement.click()
    searchStartele = wait.until(EC.presence_of_element_located((AppiumBy.ID,path["EditText"])))
    searchStartele.click()
    searchStartele.send_keys(f'{Srcmetro}')                      
    Ele = wait.until(EC.presence_of_element_located((AppiumBy.ID,path["clickStation"])))
    Ele.click()
    # set Destination
    StartpathElement = wait.until(EC.presence_of_element_located((AppiumBy.ID,path["RouteDestination"])))
    StartpathElement.click()
    searchStartele = wait.until(EC.presence_of_element_located((AppiumBy.ID,path["EditText"])))
    searchStartele.click()
    searchStartele.send_keys(f'{Dstmetro}')
    Ele = wait.until(EC.presence_of_element_located((AppiumBy.ID,path["clickStation"])))
    Ele.click()
    wait.until(EC.presence_of_element_located((AppiumBy.XPATH,fetchXPath(desired_caps["platformName"],"Show Route")))).click()
    infos = wait.until(EC.presence_of_all_elements_located((AppiumBy.ID,path["farePrice"])))
    print(f"Total Fare Amount : Rs{infos[0].text}")
    print(f"Total Fare Time : {infos[1].text}mins")
    print(f"Total Fare Stations in between : {infos[2].text}stations")
    print(f"Total Metro lines need to be change : {infos[3].text}lines")
    driver.back()
    driver.back()


# TC-6 : It verifies the first/last metro tab
@allure.description("To check whether First/Last timing of metro stations are shown or not")
def test_FirstLast():
    FirstEle = wait.until(EC.presence_of_element_located((AppiumBy.XPATH,fetchXPath(desired_caps["platformName"],"First/Last Metro"))))
    FirstEle.click()
    assert exists(Template("./images/FirstLastHeading.png"))
    print("First/Last metro tab loads successfully")
    wait.until(EC.presence_of_element_located((AppiumBy.XPATH,fetchXPath(desired_caps["platformName"],"FIRST METRO")))).click()
    wait.until(EC.presence_of_element_located((AppiumBy.ID,path["time"])))
    wait.until(EC.presence_of_element_located((AppiumBy.XPATH,fetchXPath(desired_caps["platformName"],"LAST METRO")))).click()
    wait.until(EC.presence_of_element_located((AppiumBy.ID,path["time"])))
    allure.attach(driver.get_screenshot_as_png(),name="First&LastMetro",attachment_type=attachment_type.PNG)
    driver.back()


# TC-7 : It verifies the map is visible in the upcoming tab
@allure.description("To verify upcoming metro map is showing or not")
def test_Upcoming():
    UpcomEle = wait.until(EC.presence_of_element_located((AppiumBy.XPATH,fetchXPath(desired_caps["platformName"],"Upcoming Metro"))))
    UpcomEle.click()
    assert wait.until(EC.presence_of_element_located((AppiumBy.XPATH,fetchXPath(desired_caps["platformName"],"Upcoming Metro"))))
    assert exists(Template("./images/UpcomingMetroMap.png"))
    print("Upcoming tab works fine")
    allure.attach(driver.get_screenshot_as_png(),name="UpcomingMetro",attachment_type=attachment_type.PNG)
    driver.back()


# TC-8 : It verifies whether metro stations showing parking details or not
@allure.description("To verify parking information is showing or not with respect to the metro stations.")
def test_Parking():
    ParkEle = wait.until(EC.presence_of_element_located((AppiumBy.XPATH,fetchXPath(desired_caps["platformName"],"Parking"))))
    ParkEle.click()
    assert wait.until(EC.presence_of_element_located((AppiumBy.XPATH,fetchXPath(desired_caps["platformName"],"Parking"))))
    assert exists(Template("./images/ParkingHead.png"))
    wait.until(EC.presence_of_element_located((AppiumBy.ID,path["Station"]))).click()
    metro = MetroStations[random.randint(1,40)]
    Search = wait.until(EC.presence_of_element_located((AppiumBy.ID,path["EditText"])))
    Search.click()
    time.sleep(5)
    Search.send_keys(f"{metro}")
    Ele = wait.until(EC.presence_of_element_located((AppiumBy.ID,path["clickStation"])))
    Ele.click()    
    try :
        driver.find_element(AppiumBy.XPATH,fetchXPath(desired_caps["platformName"],"CARS")).click()
        driver.find_element(AppiumBy.XPATH,fetchXPath(desired_caps["platformName"],"TWO WHEELER")).click()
        driver.find_element(AppiumBy.XPATH,fetchXPath(desired_caps["platformName"],"CYCLE")).click()
        print(f"Parking is available at {metro} station")
    except:
        driver.find_element(AppiumBy.ID,path["Parkingtxt"])
        print(f"No parking available at {metro} metro station")
    allure.attach(driver.get_screenshot_as_png(),name="Parking",attachment_type=attachment_type.PNG)
    driver.back()


# TC-9 : It checks details of entry/exit gate is showing or not with regards to metro stations
@allure.description("To verify entry/exit gates are showing or not for the metro stations.")
def test_Gates():
    GateEle = wait.until(EC.presence_of_element_located((AppiumBy.XPATH,fetchXPath(desired_caps["platformName"],"Gates and Directions"))))
    GateEle.click()
    assert wait.until(EC.presence_of_element_located((AppiumBy.XPATH,fetchXPath(desired_caps["platformName"],"Gates and Directions"))))
    assert exists(Template("./images/GateDirectionHead.png"))
    wait.until(EC.presence_of_element_located((AppiumBy.ID,path["Station"]))).click()
    allure.attach(driver.get_screenshot_as_png(),name="Gates&Directions",attachment_type=attachment_type.PNG)
    metro = MetroStations[random.randint(1,40)]
    Search = wait.until(EC.presence_of_element_located((AppiumBy.ID,path["EditText"])))
    Search.click()
    time.sleep(5)
    Search.send_keys(f"{metro}")
    Ele = wait.until(EC.presence_of_element_located((AppiumBy.ID,path["clickStation"])))
    Ele.click()
    try:
        gateNum = wait.until(EC.presence_of_all_elements_located((AppiumBy.XPATH,fetchXPath(desired_caps["platformName"],"Gate Number :"))))
        print(f"Total {len(gateNum)} gates are there on the {metro} station for Entry/Exit")
    except:
        print("No gates found")
    allure.attach(driver.get_screenshot_as_png(),name="Gates&Directions",attachment_type=attachment_type.PNG)
    driver.back()


# TC-10 : It checks the recharge tab will open browser
@allure.description("To verify recharge tab is redirecting to browser or not") 
def test_Recharge():
    RechargeEle = wait.until(EC.presence_of_element_located((AppiumBy.XPATH,fetchXPath(desired_caps["platformName"],"Card Recharge"))))
    RechargeEle.click()
    print("Recharge directed to browser")
    allure.attach(driver.get_screenshot_as_png(),name="Recharge",attachment_type=attachment_type.PNG)
    driver.activate_app(packageName)


# TC-11 : It checks the rate bar is visible or not
@allure.description("To verify the Rating screen is visible")
def test_Like():
    AdsEle = wait.until(EC.presence_of_element_located((AppiumBy.XPATH,fetchXPath(desired_caps["platformName"],"Remove Ads"))))
    ParkEle = wait.until(EC.presence_of_element_located((AppiumBy.XPATH,fetchXPath(desired_caps["platformName"],"Parking")))) 
    # For swipe the screen
    driver.scroll(ParkEle,AdsEle)
    FeedbackEle = wait.until(EC.presence_of_element_located((AppiumBy.XPATH,fetchXPath(desired_caps["platformName"],"Like this App"))))
    FeedbackEle.click()
    assert wait.until(EC.presence_of_element_located((AppiumBy.XPATH,fetchXPath(desired_caps["platformName"],"Rate this App"))))
    assert exists(Template("./images/RateApp.png"))
    print("Rating bar opened")
    allure.attach(driver.get_screenshot_as_png(),name="Like",attachment_type=attachment_type.PNG)
    driver.back()


# TC-12 : It checks the functionality of feedback tab
@allure.description("To verify screen for sharing is opening or not")
def test_Feedback():
    AdsEle = wait.until(EC.presence_of_element_located((AppiumBy.XPATH,fetchXPath(desired_caps["platformName"],"Remove Ads"))))
    ParkEle = wait.until(EC.presence_of_element_located((AppiumBy.XPATH,fetchXPath(desired_caps["platformName"],"Parking")))) 
    # For swipe the screen
    driver.scroll(ParkEle,AdsEle)
    FeedbackEle = wait.until(EC.presence_of_element_located((AppiumBy.XPATH,fetchXPath(desired_caps["platformName"],"Feedback"))))
    FeedbackEle.click()
    assert wait.until(EC.presence_of_element_located((AppiumBy.XPATH,fetchXPath(desired_caps["platformName"],"Share"))))
    print("Functionality of feedback works fine")
    allure.attach(driver.get_screenshot_as_png(),name="Feedback",attachment_type=attachment_type.PNG)
    driver.back()


# TC-13 : It checks whether about page is opening or not
@allure.description("To verify about page is opening or not")
def test_About():
    AdsEle = wait.until(EC.presence_of_element_located((AppiumBy.XPATH,fetchXPath(desired_caps["platformName"],"Remove Ads"))))
    ParkEle = wait.until(EC.presence_of_element_located((AppiumBy.XPATH,fetchXPath(desired_caps["platformName"],"Parking")))) 
    # For swipe the screen
    driver.scroll(ParkEle,AdsEle)
    AboutEle = wait.until(EC.presence_of_element_located((AppiumBy.XPATH,fetchXPath(desired_caps["platformName"],"About"))))
    AboutEle.click()
    assert wait.until(EC.presence_of_element_located((AppiumBy.XPATH,fetchXPath(desired_caps["platformName"],"Developed By:"))))
    assert exists(Template("./images/developedBy.png"))
    print("About page successfully opened")
    allure.attach(driver.get_screenshot_as_png(),name="About",attachment_type=attachment_type.PNG)
    driver.back()
    # Stop recording
    deviceRef.stop_recording()
    driver.quit()
    # Attach recording to the allure report
    video_path = "recording/Metro.mp4"
    allure.attach(open(video_path, "rb").read(), name=video_path, attachment_type=allure.attachment_type.MP4)
