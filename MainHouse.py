#!/usr/bin/env python3
"""
__authors__    = ["Blaze Sanders"]
 __contact__    = "blazes@mfc.us"
__copyright__  = "Copyright 2023"
__license__    = "GPLv3"
__status__     = "Development
__deprecated__ = False
__version__    = "0.0.1"
__doc__        = "Generate a tab based Progressive Web App GUI to control both the LiteHouse and Lustron home styles"
"""

# Disable PyLint linting messages that seem unuseful
# https://pypi.org/project/pylint/
# pylint: disable=invalid-name
# pylint: disable=global-statement

# Standard Python libraries
import sys
from time import sleep              # Enable pausing of the python program
from typing import Dict             # Enable optional data types used in creation of GUI tabs and .ENV file access
import subprocess                   # Enable the running of CLI commands like "pip3 install -r requirements.txt"
import requests                     # Grab data from the HouseAPI.py API built using FastAPI

# Internally developed modules
from PageKiteAPI import *                           # Create & delete custom subdomains for reverse proxy to tunnel
import DataProcessing as DP                         # Manage the display of NiceGUI Meraid formatted nodes
import GlobalConstants as GC                        # Global constants used across MainHouse.py, HouseDatabase.py, and PageKiteAPI.py
from HouseDatabase import HouseDatabase             # Store non-Personally Identifiable Information like house light status
from UserDataDatabase import UserDataDatabase       # Store IMPORTANT Personally Identifiable Information like physical addresses
import HouseAPI as API

# Browser base GUI framework to build and display a user interface mobile, PC, and Mac
# https://nicegui.io/
from nicegui import app, ui
from nicegui.events import MouseEventArguments

DEBUG_STATEMENTS_ON = True

try:  # Importing externally developed 3rd party modules / libraries

    # Create directory and URL for local storage of images
    if sys.platform.startswith('darwin'):
        app.add_static_files('/static/images', GC.MAC_CODE_DIRECTORY +'/static/images')
        app.add_static_files('/static/videos', GC.MAC_CODE_DIRECTORY + '/static/videos')
    elif sys.platform.startswith('linux'):
        app.add_static_files('/static/images', GC.LINUX_CODE_DIRECTORY + '/static/images')
        app.add_static_files('/static/videos', GC.LINUX_CODE_DIRECTORY + '/static/videos')
    elif sys.platform.startswith('win'):
        print("WARNING: Running MainHouse.py server code on Windows OS is NOT fully supported")
        app.add_static_files('/static/images', GC.WINDOWS_CODE_DIRECTORY + '/static/images')
        app.add_static_files('/static/videos', GC.WINDOWS_CODE_DIRECTORY + '/static/videos')
    else:
        print("ERROR: Running on an unknown operating system")
        quit()

    # Enable control of ports on an Ethernet PoE Switch using telnet
    # https://www.paramiko.org/installing.html
    import paramiko

    # Load environment variables for usernames, passwords, & API keys
    # https://pypi.org/project/python-dotenv/
    from dotenv import dotenv_values

    # Open source plaform for NoSQL databases, authentication, file storage, and auto-generated APIs
    # https://github.com/supabase-community/supabase-py
    from supabase.client import create_client, Client

    # Reverse lookup a street address from GPS and vice verse & GeoLocate based on cell towers and wifi
    # https://github.com/googlemaps/google-maps-services-python
    # https://developers.google.com/maps/documentation/geolocation/overview
    # import googlemaps

except ImportError:
    print("ERROR: Not all the required libraries are installed!")
    executeInstalls = input("Would you like me to *** pip3 install -r requirements.txt *** into Virtual Enviroment for you (Y/N)? ")

    # If code is running on Linux or MacOS create Virtual Enviroment and required pip installs
    if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        if(executeInstalls.upper() == "Y" or executeInstalls.upper() == "YES"):
            subprocess.call(['sudo', 'apt', 'install', 'python3-venv'])
            subprocess.call(['python3', '-m', 'venv', '.VENV'])
            subprocess.call(['source', '.VENV/bin/activate'])
            subprocess.call(['sudo', 'apt', 'install', 'python3-pip'])
            subprocess.call(['pip3', 'install', '-r', 'requirements.txt'])
    else:
        print("You didn't type Y or YES :)")
        print("Manually install Python3.9 or higher and ")

finally:
    # Global Variables
    isDarkModeOn = False            # Application boots up in light mode
    darkMode = ui.dark_mode()

    userLoggedIn = False
    sanitizedPhoneNumber = '5555555555'
    sanitizedOtpCode = '123456'
    username = sanitizedPhoneNumber

    isMasterBedroomLightsOn = False
    isMasterBathroomLightsOn = False
    isKitchenLightsOn = False
    isLivingRoomLightsOn = False
    isHallwayLightsOn = False
    isAreaLightOn = [isHallwayLightsOn, isLivingRoomLightsOn, isKitchenLightsOn, isMasterBedroomLightsOn, isMasterBathroomLightsOn]    #TODO Add more areas (e.g. rooms, closets, porches) for other Litehouse and Lustron rooms
    liteHouseLightState = 0b0000_0000
    
    isMasterBathroomFanOn = False
    isMasterBathroomFanOn = False
    isAreaFanOn = [False, False, False, isMasterBathroomFanOn, isMasterBathroomFanOn]           #TODO Add more areas (e.g. rooms, closets, porches) for other Litehouse and Lustron rooms
    liteHouseFanState = 0b0000_0000


    # TODO Remove Lustron from MainHouse.py and rename to MainLiteHouse.py???
    houseType = GC.LITE_HOUSE_SOURCE                            # 2nd option is GC.LUSTRON_SOURCE
    lustronLightState = 0b00000_0000_0000_0000
    
    homeName = 'MyHouse'
    homeAddress = '407 E Central Blvd, Orlando, FL 32801'
    litehousePageKiteDomain = 'litehouse.pagekite.me'
    lustronPageKiteDomain = 'lustron.pagekite.me'
    tabNames = ['lights', 'cameras', 'doors', 'network']



def toggle_dark_mode():
    """ Toggle entire window between light mode and dark mode
    """
    global isDarkModeOn

    if isDarkModeOn:
        darkMode.disable()
    else:
        darkMode.enable()

    isDarkModeOn = not isDarkModeOn


def login_user():
    global userLoggedIn 
    # https://github.com/zauberzeug/nicegui/tree/main/examples/nginx_subpath/
    userLoggedIn = not userLoggedIn
    userDataForm.visible = userLoggedIn
    ui.update(userDataForm)


def send_otp_password(phoneNumber: str, invalidPhoneNumberLabel: ui.label, enterPhoneNumberGrid: ui.grid):
    """ Send a random 6 digit code via SMS and edit GUI elements in real time if input conatins formatting errors

    Args:
        phoneNumber (String): Valid 10 digit phone number from US and Canada (https://www.iban.com/dialing-codes) 
        invalidPhoneNumberLabel (ui.label): GUI label element 
        enterPhoneNumberGrid (ui.grid): GUI grid (a collection of label & input)
    """
    global username

    isValidPhoneNumber = True
    countryCodePhoneNumber = '+1' + phoneNumber

    if len(phoneNumber) < 10:
        isValidPhoneNumber = False

    if not isValidPhoneNumber:
        invalidPhoneNumberLabel.set_text(phoneNumber + ' is not a valid number')
        invalidPhoneNumberLabel.tailwind.font_weight('extrabold').text_color('red-600')
        invalidPhoneNumberLabel.visible = True
    else:
        try:
            response = supabase.auth.sign_in_with_otp({"phone": countryCodePhoneNumber,})
            print(f'Supabase called to send SMS: {response}')

        finally:
            enterPhoneNumberGrid.visible = False
            signInGrid.visible = True
            username = countryCodePhoneNumber


def sign_in(sanitizedOtpCode, invalidOtpLabel, signInGrid):
    global username
    print(f'ATTEMPTING SIGN IN WITH username: {username} with {sanitizedOtpCode}')

    validUser = supabase.auth.verify_otp({"phone": username, "token": str(sanitizedOtpCode), "type": 'sms'})
    db1.insert_debug_logging_table(f'Supabase called to verify OTP: USER = {validUser}') 

    if validUser.user.aud == 'authenticated':
        db1.insert_users_table(username, sanitizedOtpCode)

    if db1.verify_password(username, sanitizedOtpCode):
        userFound = True
    else:
        userFound = False

    if userFound:
        userDataForm.visible = True
        signInGrid.visible = False
    else:
        invalidOtpLabel.set_text(sanitizedOtpCode + ' is not a valid OTP code')
        invalidOtpLabel.tailwind.font_weight('extrabold').text_color('red-600')
        invalidOtpLabel.visible = True

    # TODO Force user to give home a unquie name
    # Add this new subdomain to database and use a session JWT (Java Web Token)


def reset_login_gui(invalidPhoneNumberLabel, enterPhoneNumberGrid, signInGrid, userDataForm):
    """ Toggle the visibility of labels and grid in the left drawer to reset GUI to boot state

    Args:
        invalidPhoneNumberLabel (ui.label()): _description_
        enterPhoneNumberGrid (ui.grid()): _description_
        signInGrid (ui.grid()): _description_
        userDataForm (ui.grid()): _description_
    """
    supabase.auth.sign_out()
    invalidPhoneNumberLabel.visible = False
    invalidOtpLabel.visible = False
    enterPhoneNumberGrid.visible = True
    signInGrid.visible = False
    userDataForm.visible = False


def switch_tab(msg: Dict) -> None:
    name = msg['args']
    tabs.props(f'model-value={name}')
    panels.props(f'model-value={name}')


def sanitize_phone_number(text):
    global sanitizedPhoneNumber

    sanitizedPhoneNumber = text.replace(" ", "")
    sanitizedPhoneNumber = sanitizedPhoneNumber.replace("(", "")
    sanitizedPhoneNumber = sanitizedPhoneNumber.replace(")", "")
    sanitizedPhoneNumber = sanitizedPhoneNumber.replace(".", "")
    sanitizedPhoneNumber = sanitizedPhoneNumber.replace("-", "")
    sanitizedPhoneNumber = sanitizedPhoneNumber.replace("+", "")

    invalidPhoneNumberLabel.visible = False

    return sanitizedPhoneNumber

def sanitize_otp_code(text) -> str:
    global sanitizedOtpCode
    
    sanitizedOtpCode = text.replace(" ", "")
    sanitizedOtpCode = sanitizedOtpCode.replace("-", "")
    
    return sanitizedOtpCode

def determine_room_fan_mouse_handler(e: MouseEventArguments):
    global isMasterBedroomFanOn
    global ismasterBathroomFanOn
    
    print(isMasterBedroomFanOn)


def determine_room_light_mouse_handler(e: MouseEventArguments):
    global isMasterBedroomLightsOn
    global isMasterBathroomLightsOn
    global isKitchenLightsOn
    global isLivingRoomLightsOn
    global isHallwayLightsOn

    areaFound = False

    for areaIndex in range(GC.MAX_AREA_INDEX_MASTER_BEDROOM):
        if GC.MASTER_BEDROOM_X[areaIndex] <= e.image_x <= GC.MASTER_BEDROOM_X[areaIndex] + GC.MASTER_BEDROOM_X_WIDTH[areaIndex] and \
           GC.MASTER_BEDROOM_Y[areaIndex] <= e.image_y <= GC.MASTER_BEDROOM_Y[areaIndex] + GC.MASTER_BEDROOM_Y_HEIGHT[areaIndex]:

            areaFound = True
            isMasterBedroomLightsOn = not isMasterBedroomLightsOn
            if isMasterBedroomLightsOn:
                ui.notify(message='Please wait turning Master Bedroom lights ON')
                
                if GC.SWITH_HARDWARE_CONNECTED:
                    # Telnet command
                    telnet_command = f'(echo "enable" ; echo "configure" ; echo "interface \'0/{GC.MASTER_BEDROOM_SWITCH_PORT}\'" ; echo "poe opmode auto" ; echo "exit" ; echo "exit" ; echo "exit") | telnet localhost 23 ; exit;'
                    stdin, stdout, stderr = ssh.exec_command(telnet_command)
                    print(stdout.read().decode())

            else:
                ui.notify(message='Master Bedroom lights OFF')
                
                if GC.SWITH_HARDWARE_CONNECTED:
                    # Telnet command
                    telnet_command = f'(echo "enable" ; echo "configure" ; echo "interface \'0/{GC.MASTER_BEDROOM_SWITCH_PORT}\'" ; echo "poe opmode shutdown" ; echo "exit" ; echo "exit" ; echo "exit") | telnet localhost 23 ; exit;'
                    stdin, stdout, stderr = ssh.exec_command(telnet_command)
                    output = stdout.read().decode()
                    print(output)

            draw_light_highlight(ii, isMasterBedroomLightsOn, GC.MASTER_BEDROOM)
            
    

    for areaIndex in range(GC.MAX_AREA_INDEX_MASTER_BATHROOM):
        if GC.MASTER_BATHROOM_X[areaIndex] <= e.image_x <= GC.MASTER_BATHROOM_X[areaIndex] + GC.MASTER_BATHROOM_X_WIDTH[areaIndex] and \
           GC.MASTER_BATHROOM_Y[areaIndex] <= e.image_y <= GC.MASTER_BATHROOM_Y[areaIndex] + GC.MASTER_BATHROOM_Y_HEIGHT[areaIndex]:

            areaFound = True
            isMasterBathroomLightsOn = not isMasterBathroomLightsOn
            if isMasterBathroomLightsOn:
                ui.notify(message='Please wait turning Bathroom lights ON')

                if GC.SWITH_HARDWARE_CONNECTED:
                    # Telnet command
                    telnet_command = f'(echo "enable" ; echo "configure" ; echo "interface \'0/{GC.MASTER_BATHROOM_SWITCH_PORT}\'" ; echo "poe opmode auto" ; echo "exit" ; echo "exit" ; echo "exit") | telnet localhost 23 ; exit;'
                    stdin, stdout, stderr = ssh.exec_command(telnet_command)
                    print(stdout.read().decode())

            else:
                ui.notify(message='Bathroom lights OFF')
                
                if GC.SWITH_HARDWARE_CONNECTED:
                    # Telnet command
                    telnet_command = f'(echo "enable" ; echo "configure" ; echo "interface \'0/{GC.MASTER_BATHROOM_SWITCH_PORT}\'" ; echo "poe opmode shutdown" ; echo "exit" ; echo "exit" ; echo "exit") | telnet localhost 23 ; exit;'
                    stdin, stdout, stderr = ssh.exec_command(telnet_command)
                    print(stdout.read().decode())

            draw_light_highlight(ii, isMasterBathroomLightsOn, GC.MASTER_BATHROOM)
    
    
    for areaIndex in range(GC.MAX_AREA_INDEX_KITCHEN):
        if GC.KITCHEN_X[areaIndex] <= e.image_x <= GC.KITCHEN_X[areaIndex] + GC.KITCHEN_X_WIDTH[areaIndex] and \
           GC.KITCHEN_Y[areaIndex] <= e.image_y <= GC.KITCHEN_Y[areaIndex] + GC.KITCHEN_Y_HEIGHT[areaIndex]:

            areaFound = True
            isKitchenLightsOn = not isKitchenLightsOn
            if isKitchenLightsOn:
                ui.notify(message='Please wait turning Kitchen lights ON')

                if GC.SWITH_HARDWARE_CONNECTED:
                    # Telnet command
                    telnet_command = f'(echo "enable" ; echo "configure" ; echo "interface \'0/{GC.KITCHEN_SWITCH_PORT}\'" ; echo "poe opmode auto" ; echo "exit" ; echo "exit" ; echo "exit") | telnet localhost 23 ; exit;'
                    stdin, stdout, stderr = ssh.exec_command(telnet_command)
                    print(stdout.read().decode())

            else:
                ui.notify(message='Kitchen lights OFF')
                
                if GC.SWITH_HARDWARE_CONNECTED:
                    # Telnet command
                    telnet_command = f'(echo "enable" ; echo "configure" ; echo "interface \'0/{GC.KITCHEN_SWITCH_PORT}\'" ; echo "poe opmode shutdown" ; echo "exit" ; echo "exit" ; echo "exit") | telnet localhost 23 ; exit;'
                    stdin, stdout, stderr = ssh.exec_command(telnet_command)
                    print(stdout.read().decode())

            draw_light_highlight(ii, isKitchenLightsOn, GC.KITCHEN)
    
    
    for areaIndex in range(GC.MAX_AREA_INDEX_LIVINGROOM):
        if GC.LIVINGROOM_X[areaIndex] <= e.image_x <= GC.LIVINGROOM_X[areaIndex] + GC.LIVINGROOM_X_WIDTH[areaIndex] and \
           GC.LIVINGROOM_Y[areaIndex] <= e.image_y <= GC.LIVINGROOM_Y[areaIndex] + GC.LIVINGROOM_Y_HEIGHT[areaIndex]:

            areaFound = True
            isLivingRoomLightsOn = not isLivingRoomLightsOn
            if isLivingRoomLightsOn:
                ui.notify(message='Please wait turning Living Room lights ON')

                if GC.SWITH_HARDWARE_CONNECTED:
                    # Telnet command
                    telnet_command = f'(echo "enable" ; echo "configure" ; echo "interface \'0/{GC.LIVINGROOM_SWITCH_PORT}\'" ; echo "poe opmode auto" ; echo "exit" ; echo "exit" ; echo "exit") | telnet localhost 23 ; exit;'
                    stdin, stdout, stderr = ssh.exec_command(telnet_command)
                    print(stdout.read().decode())

            else:
                ui.notify(message='Kitchen lights OFF')
                
                if GC.SWITH_HARDWARE_CONNECTED:
                    # Telnet command
                    telnet_command = f'(echo "enable" ; echo "configure" ; echo "interface \'0/{GC.LIVINGROOM_SWITCH_PORT}\'" ; echo "poe opmode shutdown" ; echo "exit" ; echo "exit" ; echo "exit") | telnet localhost 23 ; exit;'
                    stdin, stdout, stderr = ssh.exec_command(telnet_command)
                    print(stdout.read().decode())

            draw_light_highlight(ii, isLivingRoomLightsOn, GC.LIVINGROOM)
    
    for areaIndex in range(GC.MAX_AREA_INDEX_HALLWAY):
        if GC.HALLWAY_X[areaIndex] <= e.image_x <= GC.HALLWAY_X[areaIndex] + GC.HALLWAY_X_WIDTH[areaIndex] and \
           GC.HALLWAY_Y[areaIndex] <= e.image_y <= GC.HALLWAY_Y[areaIndex] + GC.HALLWAY_Y_HEIGHT[areaIndex]:

            areaFound = True
            isHallwayLightsOn = not isHallwayLightsOn
            if isHallwayLightsOn:
                ui.notify(message='Please wait turning Hallway lights ON')

                if GC.SWITH_HARDWARE_CONNECTED:
                    # Telnet command
                    telnet_command = f'(echo "enable" ; echo "configure" ; echo "interface \'0/{GC.HALLWAY_SWITCH_PORT}\'" ; echo "poe opmode auto" ; echo "exit" ; echo "exit" ; echo "exit") | telnet localhost 23 ; exit;'
                    stdin, stdout, stderr = ssh.exec_command(telnet_command)
                    print(stdout.read().decode())

            else:
                ui.notify(message='Kitchen lights OFF')
                
                if GC.SWITH_HARDWARE_CONNECTED:
                    # Telnet command
                    telnet_command = f'(echo "enable" ; echo "configure" ; echo "interface \'0/{GC.HALLWAY_SWITCH_PORT}\'" ; echo "poe opmode shutdown" ; echo "exit" ; echo "exit" ; echo "exit") | telnet localhost 23 ; exit;'
                    stdin, stdout, stderr = ssh.exec_command(telnet_command)
                    print(stdout.read().decode())

            draw_light_highlight(ii, isHallwayLightsOn, GC.HALLWAY)
    
    db1.update_light_state_table(liteHouseLightState)
    

    if not areaFound:
        print("Clicked outside Master Bedroom and Bathroom areas")
        ui.notify(f'{e.type} at ({e.image_x:.1f}, {e.image_y:.1f})')

    
def draw_light_highlight(ii, isLightOn, roomName):
    global liteHouseLightState
    global lustronLightState

    if DEBUG_STATEMENTS_ON: print(f'Light State BEFORE click: {bin(liteHouseLightState)}')

    # Define the light state modifications for each room
    roomLightModificationsDict = {
        GC.MASTER_BEDROOM: (0b0000_0001, 0b1111_1110),
        GC.MASTER_BATHROOM: (0b0000_0010, 0b1111_1101),
        GC.KITCHEN: (0b0000_0100, 0b1111_1011),
        GC.LIVINGROOM: (0b0000_1000, 0b1111_0111),
        GC.HALLWAY: (0b0001_0000, 0b1110_1111),
        # Add more rooms and their corresponding modifications as needed
        GC.BEDROOM_2: (0b0000_0101, 0b1111_1010), 
    }

    if roomName in roomLightModificationsDict:
        light_on_mask, light_off_mask = roomLightModificationsDict[roomName]
        if isLightOn:
            liteHouseLightState |= light_on_mask
        else:
            liteHouseLightState &= light_off_mask

    if DEBUG_STATEMENTS_ON: print(f'Light State AFTER click: " {bin(liteHouseLightState)}')

    if houseType == GC.LITE_HOUSE_SOURCE:

        if liteHouseLightState == 0b0000_0000:   ii.set_source(GC.LITE_HOUSE_SOURCE)
        elif liteHouseLightState == 0b0000_0001: ii.set_source(GC.LITE_HOUSE_SOURCE00000001)
        elif liteHouseLightState == 0b0000_0010: ii.set_source(GC.LITE_HOUSE_SOURCE00000010)
        elif liteHouseLightState == 0b0000_0011: ii.set_source(GC.LITE_HOUSE_SOURCE00000011)
        elif liteHouseLightState == 0b0000_0100: ii.set_source(GC.LITE_HOUSE_SOURCE00000100)
        elif liteHouseLightState == 0b0000_0101: ii.set_source(GC.LITE_HOUSE_SOURCE00000101)
        elif liteHouseLightState == 0b0000_0110: ii.set_source(GC.LITE_HOUSE_SOURCE00000110)
        elif liteHouseLightState == 0b0000_0111: ii.set_source(GC.LITE_HOUSE_SOURCE00000111)
        elif liteHouseLightState == 0b0000_1000: ii.set_source(GC.LITE_HOUSE_SOURCE00001000)
        elif liteHouseLightState == 0b0000_1001: ii.set_source(GC.LITE_HOUSE_SOURCE00001001)
        elif liteHouseLightState == 0b0000_1010: ii.set_source(GC.LITE_HOUSE_SOURCE00001010)
        elif liteHouseLightState == 0b0000_1011: ii.set_source(GC.LITE_HOUSE_SOURCE00001011)
        elif liteHouseLightState == 0b0000_1100: ii.set_source(GC.LITE_HOUSE_SOURCE00001100)
        elif liteHouseLightState == 0b0000_1101: ii.set_source(GC.LITE_HOUSE_SOURCE00001101)
        elif liteHouseLightState == 0b0000_1110: ii.set_source(GC.LITE_HOUSE_SOURCE00001110)
        elif liteHouseLightState == 0b0000_1111: ii.set_source(GC.LITE_HOUSE_SOURCE00001111) 
        elif liteHouseLightState == 0b0001_0000: ii.set_source(GC.LITE_HOUSE_SOURCE00010000)
        elif liteHouseLightState == 0b0001_0001: ii.set_source(GC.LITE_HOUSE_SOURCE00010001)
        elif liteHouseLightState == 0b0001_0010: ii.set_source(GC.LITE_HOUSE_SOURCE00010010)        
        elif liteHouseLightState == 0b0001_0011: ii.set_source(GC.LITE_HOUSE_SOURCE00010011)
        elif liteHouseLightState == 0b0001_0100: ii.set_source(GC.LITE_HOUSE_SOURCE00010100)
        elif liteHouseLightState == 0b0001_0101: ii.set_source(GC.LITE_HOUSE_SOURCE00010101)
        elif liteHouseLightState == 0b0001_0110: ii.set_source(GC.LITE_HOUSE_SOURCE00010110)        
        elif liteHouseLightState == 0b0001_0111: ii.set_source(GC.LITE_HOUSE_SOURCE00010111)        
        elif liteHouseLightState == 0b0001_1000: ii.set_source(GC.LITE_HOUSE_SOURCE00011000)        
        elif liteHouseLightState == 0b0001_1001: ii.set_source(GC.LITE_HOUSE_SOURCE00011001)
        elif liteHouseLightState == 0b0001_1010: ii.set_source(GC.LITE_HOUSE_SOURCE00011010)        
        elif liteHouseLightState == 0b0001_1011: ii.set_source(GC.LITE_HOUSE_SOURCE00011011)        
        elif liteHouseLightState == 0b0001_1100: ii.set_source(GC.LITE_HOUSE_SOURCE00011100)        
        elif liteHouseLightState == 0b0001_1101: ii.set_source(GC.LITE_HOUSE_SOURCE00011101)        
        elif liteHouseLightState == 0b0001_1110: ii.set_source(GC.LITE_HOUSE_SOURCE00011110)        
        elif liteHouseLightState == 0b0001_1111: ii.set_source(GC.LITE_HOUSE_SOURCE00011111)
        else: ui.notify(message='INVALID LIGHT STATE: Refresh your browser window')        
                                               
    elif houseType == GC.LUSTRON_SOURCE:
        """ CAN"T USE match until python3.11 can be installed on Zimaboard
        match lustronLightState:
            case 0b0000_0000:
                ii.set_source(GC.LUSTRON_SOURCE)
            case _:
                ui.notify(message='INVALID LIGHT STATE: Refresh your browser window')
        """
        pass
    else:
        db1.insert_error_logging_table(f'ERROR: Invalid House Type - Light status images was not updated / displayed')

def start_api() -> int:
    """Use UVicorn a fast ASGI (Asynchronous Server Gateway Interface) to running auto refreshing API
    """
    
    command = ['uvicorn', 'HouseAPI:app', '--host', '0.0.0.0', '--reload', '--port', API.API_PORT]
    backgroundApiProcess = subprocess.Popen(command)
    processCode = backgroundApiProcess.pid
    print(f'PID = {processCode}')
    sleep(3)       # Delay to give API server kill to start up
    
    return int(processCode)

async def show_location():
    response = await ui.run_javascript('''
        return await new Promise((resolve, reject) => {
            if (!navigator.geolocation) {
                reject(new Error('Geolocation is not supported by your browser'));
            } else {
                navigator.geolocation.getCurrentPosition(
                    (position) => {
                        resolve({
                            latitude: position.coords.latitude,
                            longitude: position.coords.longitude,
                        });
                    },
                    () => {
                        reject(new Error('Unable to retrieve your location'));
                    }
                );
            }
        });
    ''', timeout=5.0)
    return response["latitude"], response["longitude"] #ui.notify(f'Your location is {response["latitude"]}, {response["longitude"]}')


if __name__ in {"__main__", "__mp_main__"}:
    darkMode.disable()

    db1 = HouseDatabase()

    if __name__ == "__main__":
        # Outgoing API connection should only run once, on single port, in a single threaded main function
        apiBackgroundProcessCode = start_api()

    # Incoming APIs
    try:
        config = dotenv_values()
    except KeyError:
        db1.insert_error_logging_table(GC.USER_TABLE, "ERROR: Could not find .ENV file")
    finally:
        url = config['SUPABASE_URL']
        key = config['SUPABASE_KEY']
        supabase: Client = create_client(url, key)

        #pageKite = PageKiteAPI('litehouse.pagekite.me', config, db1)
        #serveApp = PageKiteStartUp(homeName)

        # Establish SSH connection with UniFi PoE Ethernet Switch
        if GC.SWITH_HARDWARE_CONNECTED:
            unifiSshUserName = config['USERNAME_UNIFI_USW_ENTERPRISE_24_POE']
            unifiSshpw = config['PASSWORD_UNIFI_USW_ENTERPRISE_24_POE']

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect('192.168.100.160', username=unifiSshUserName, password=unifiSshpw)

    
        
    try:
        # NiceGUI code runing in "__mp_main__"
        ui.colors(primary=GC.MAMMOTH_BRIGHT_GRREN)
        
        with ui.header().classes(replace='row items-center') as header:
            ui.button(on_click=lambda: left_drawer.toggle()).props('flat color=white icon=home')
            with ui.element('q-tabs').on('update:model-value', switch_tab) as tabs:
                for name in tabNames:
                    ui.element('q-tab').props(f'name={name} label={name}')

        with ui.footer(value=False) as footer:
            ui.label('Mammoth Factory Corp')


        with ui.left_drawer().classes('bg-white-100') as left_drawer:
            with ui.grid(columns=1):
                darkModeSwitch = ui.switch('Enable Dark Mode', on_change=toggle_dark_mode)
                ui.label('')
                
                enterPhoneNumberGrid = ui.grid(columns=1)
                with enterPhoneNumberGrid:
                    
                    
                    invalidPhoneNumberLabel = ui.label()
                    invalidPhoneNumberLabel.visible = False
                    userInputTextBox = ui.input(label='Enter your 10 digit phone number', placeholder='e.g. 7195551234', \
                                    on_change=lambda e: invalidPhoneNumberLabel.set_text(sanitize_phone_number(e.value)), \
                                    validation={'Phone number is too long': lambda value: len(sanitizedPhoneNumber) <= GC.VALID_USA_CANADA_MEXICO_PHONE_NUMBER_LENGTH})  # Length incluses + symbol at start of phone number
                    
                    userInputButton = ui.button('NEXT', on_click=lambda e: send_otp_password(sanitizedPhoneNumber, invalidPhoneNumberLabel, enterPhoneNumberGrid))
                    
                    ui.label('')
                    ui.label('')
                
            
                signInGrid = ui.grid(columns=1)
                signInGrid.visible = False
                with signInGrid:
                    invalidOtpLabel = ui.label()
                    invalidOtpLabel.visible = False
                    optInputTextBox = ui.input(label='Enter 6 digit code', placeholder='e.g. 123456', \
                            on_change=lambda e: invalidOtpLabel.set_text(sanitize_otp_code(e.value)), \
                            validation={'Code too long, should be 6 digits': lambda value: len(sanitizedOtpCode) <= 6})
                    
                    signInButton = ui.button('SIGN IN', on_click=lambda e: sign_in(sanitizedOtpCode, invalidOtpLabel, signInGrid))

            userDataForm = ui.grid(columns=2)
            userDataForm.visible = False
            with userDataForm:
                ui.label('Home Name:').tailwind.font_weight('extrabold')
                ui.label(homeName).style('gap: 10px')
            
                ui.label('Home Address:').tailwind.font_weight('extrabold')
                ui.label(homeAddress)

                ui.label('Home GPS:').tailwind.font_weight('extrabold')
                ui.label("28.54250516114, -81.372488625")
                
                signOutButton = ui.button('SIGN OUT', on_click=lambda e: reset_login_gui(invalidPhoneNumberLabel, enterPhoneNumberGrid, signInGrid, userDataForm))


        with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
            infoButton = ui.button(on_click=footer.toggle).props('fab icon=info')

        
        # the page content consists of multiple tab panels
        with ui.element('q-tab-panels').props('model-value=A animated').classes('w-full') as panels:
            #for name in tabNames:
            
        
            with ui.element('q-tab-panel').props(f'name={tabNames[0]}').classes('w-full'):
                with ui.grid(columns=1):
                    ui.label(f'Click on image to toggle {tabNames[0]}').tailwind('mx-auto text-2xl')
                    ii = ui.interactive_image(houseType, on_mouse=determine_room_light_mouse_handler, events=['mousedown'], cross=True)
                    
            with ui.element('q-tab-panel').props(f'name={tabNames[1]}').classes('w-full'):
                with ui.grid(columns=1):
                    ui.image('https://picsum.photos/id/377/640/360')
                    
            with ui.element('q-tab-panel').props(f'name={tabNames[2]}').classes('w-full'):
                with ui.grid(columns=2):
                    ui.image('static/images/OpenDoor.gif')
                    
                    ui.image('static/images/OpenDoor.gif')
                            
            with ui.element('q-tab-panel').props(f'name={tabNames[3]}').classes('w-full'):
                with ui.grid(columns=1):
                    ui.label(f'{tabNames[3].capitalize()} Layout').tailwind('mx-auto text-2xl')
                    # WORKS!!! :) newNetworkDiagram = DP.output_network_diagram(DP.delete_network_diagram_node(DP.parse_network_diagram(DP.STATIC_DEFAULT_NETWORK), 'H'))
                    newNetworkDiagram = DP.STATIC_DEFAULT_NETWORK
                    ui.mermaid(newNetworkDiagram)
                    
        ui.run(native=GC.RUN_ON_NATIVE_OS, port=GC.LOCAL_HOST_PORT_FOR_GUI)
        
    except KeyboardInterrupt:
        command = ['kill', '-9', str(apiBackgroundProcessCode)]
        subprocess.call(command)
