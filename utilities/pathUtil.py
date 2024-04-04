packageName = 'com.tilzmatictech.mobile.navigation.delhimetronavigator'
MetroStations = {
    1 : 'AIIMS',
    2 : 'Adarsh Nagar',
    3 : 'Airport',
    4 : 'Akshardham',
    5 : 'Alpha',
    6 : 'Anand Vihar ISBT',
    7 : 'Arjan Garh',
    8 : 'Arthala',
    9 : 'Ashok Park Main',
    10 : 'Ashram',
    11 : 'Azadpur',
    12 : 'Badarpur Border',
    13 : 'Badkal Mor',
    14 : 'Bahadurgarh City',
    15 : 'Barakhamba Road',
    16 : 'Bata Chowk',
    17 : 'Golf Course',
    18 : 'Bhikaji Cama Place',
    19 : 'Botanical Garden',
    20 : 'Brigadier Hoshiar Singh',
    21 : 'Central Secretariat',
    22 : 'Chandni Chowk',
    23 : 'Chawri Bazar',
    24 : 'Chhatarpur',
    25 : 'Chirag Delhi',
    26 : 'Civil Lines',
    27 : 'ITO',
    28 : 'Dabri Mor',
    29 : 'Dashrath Puri',
    30 : 'Janpath',
    31 : 'Delhi Aerocity',
    32 : 'Delhi Cantt',
    33 : 'Delhi Gate',
    34 : 'Delta 1',
    35 : 'Depot Station',
    36 : 'Dhansa Bus Stand',
    37 : 'Dhaula Kuan',
    38 : 'East Azad Nagar',
    39 : 'Gokulpuri',
    40 : 'Green Park',
    41 : 'Majlis Park',
    42 : 'Vidhan Sabha',
    43 : 'Rajdhani Park',
    44 : 'Hindon River'
}

path = {
    "Remove Ads" : "Remove Ads",
    "Fare" : "Fare",
    "Show Fare" : "Show Fare",
    "Map" : "Map",
    "Route" : "Route",
    "Show Route" : "Show Route",
    "FIRST METRO" : "FIRST METRO",
    "LAST METRO" : "LAST METRO",
    "Upcoming Metro" : "Upcoming Metro",
    "Parking" : "Parking",
    "CARS" : "CARS",
    "TWO WHEELER" : "TWO WHEELER",
    "CYCLE" : "CYCLE",
    "Gates and Directions" : "Gates and Directions",
    "Card Recharge" : "Card Recharge",
    "Like this App" : "Like this App",
    "Rate this App" : "Rate this App",
    "Feedback" : "Feedback",
    "Share" : "Share",
    "About" : "About",
    "Developed By:" : "Developed By:",
    "Gate Number :" : "Gate Number :",
    "First/Last Metro" : "First/Last Metro",
    "Delhi Metro Navigator" : "Delhi Metro Navigator",
    "FareSource" : packageName+":id/src_search_icon",
    "FareDestination" : packageName+":id/dst_search_icon",
    "EditText" : packageName+":id/edittxt_select_item",
    "clickStation" : packageName+":id/station_info",
    "farePrice" : packageName+":id/txt_data",
    "RouteSource" : packageName+":id/txt_source",
    "RouteDestination" : packageName+":id/txt_destination",
    "time" : packageName+":id/time",
    "Parking" : packageName+":id/txt_parking",
    "Station" : packageName+":id/txt_station",

}

def fetchXPath(device,text,contain=0):
    print(device)
    if device == "Android":
        if contain == 0:
            return f"//android.widget.TextView[@text='{path[text]}']"
        else:
            return f"//android.widget.TextView[contains('@text','{text}')]"
    elif device == "iOS":
        if contain == 0:
            return f"//XCUIElementTypeStaticText[@name='{path[text]}']"
        else:
            return f"//XCUIElementTypeStaticText[contains('@name','{text}')]"    
