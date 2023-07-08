#!/usr/bin/env python3
"""
__authors__    = ["Blaze Sanders"]
__contact__    = "blaze.d.a.sanders@gmail.com"
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
from datetime import datetime       # TODO Remove if not used
from typing import Dict             # Enable optional data types used in creation of GUI tabs
import subprocess                   # Enable the running of CLI commands like "pip3 install -r requirements.txt"
from dotenv import dotenv_values    # Load environment variables for usernames, passwords, & API keys
import requests                     # Grab data from the HouseAPI.py API built using FastAPI

# Internally developed modules
from PageKiteAPI import *                           # Create & delete custom subdomains for reverse proxy to tunnel
import DataProcessing as DP                         # Manage the display of NiceGUI Meraid formatted nodes
import GlobalConstants as GC                        # Global constants used in MainHouse.py, 
from HouseDatabase import HouseDatabase             # Store non-Personally Identifiable Information like house light status
from UserDataDatabase import UserDataDatabase       # Store IMPORTANT Personally Identifiable Information like physical addresses
import HouseAPI as API


try:  # Importing externally developed 3rd party modules / libraries

    # Browser GUI framework to build and display a user interface on the internet
    # https://nicegui.io/
    from nicegui import app, ui
    from nicegui.events import MouseEventArguments

    # Create directory and URL for local storage of images
    if sys.platform.startswith('darwin'):
        app.add_static_files('/static/images', GC.MAC_CODE_DIRECTORY +'/static/images')
        app.add_static_files('/static/videos', GC.MAC_CODE_DIRECTORY + '/static/videos')
    elif sys.platform.startswith('linux'):
        app.add_static_files('/static/images', GC.LINUX_CODE_DIRECTORY + '/static/images')
        app.add_static_files('/static/videos', GC.LINUX_CODE_DIRECTORY + '/static/videos')
    elif sys.platform.startswith('win'):
        print("ERROR: Running on Windows is NOT supported")
    else:
        print("ERROR: Running on an unknown operating system")

    # Enable control of ports on an Ethernet PoE Switch using telnet
    # https://www.paramiko.org/installing.html
    import paramiko
    
    # Open source plaform for NoSQL databases, authentication, file storage, and auto-generated APIs
    # https://github.com/supabase-community/supabase-py
    #import supabase
    from supabase import create_client, Client

    # Reverse lookup a street address from GPS and vice verse & GeoLocate based on cell towers and wifi
    # https://github.com/googlemaps/google-maps-services-python
    # https://developers.google.com/maps/documentation/geolocation/overview
    import googlemaps

except ImportError:
    print("ERROR: Not all the required libraries are installed!")
    executeInstalls = input("Would you like me to *** pip3 install -r requirements.txt *** into Virtual Enviroment for you (Y/N)? ")
    if(executeInstalls.upper() == "Y" or executeInstalls.upper() == "YES"):
        subprocess.call(['Python3', '-m', 'venv', '.VENV'])
        subprocess.call(['source', '.VENV/bin/activate'])
        subprocess.call(['sudo', 'apt', 'install', 'python3-pip'])
        subprocess.call(['pip3', 'install', '-r', 'requirements.txt'])
    else:
        print("You didn't type Y or YES :)")
        print("Manually install Python3.9 or higher and ")

# Global Variables
isDarkModeOn = False            # Application boots up in light mode
darkMode = ui.dark_mode()       

userLoggedIn = False
sanitizedPhoneNumber = '5555555555'
sanitizedOtpCode = '123456'
username = sanitizedPhoneNumber

isMasterBedroomLightsOn = False
ismasterBathroomLightsOn = False
houseType = GC.LITE_HOUSE_SOURCE                            # 2nd option is GC.LUSTRON_SOURCE
liteHouseLightState = 0b0000_0000
lustronLightState = 0b0000_0000
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

    userLoggedIn = not userLoggedIn
    userDataForm.visible = userLoggedIn
    ui.update(userDataForm)


def send_otp_password(phoneNumber, invalidPhoneNumberLabel, enterPhoneNumberGrid):
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
            user = supabase.auth.sign_in_with_otp({"phone": countryCodePhoneNumber,})
        finally:
            enterPhoneNumberGrid.visible = False
            signInGrid.visible = True
            username = countryCodePhoneNumber


def sign_in(sanitizedOtpCode, invalidOtpLabel, signInGrid):
    global username
    print(f'ATTEMPTING SIGN IN WITH username: {username} with {sanitizedOtpCode}')
    
    res = supabase.auth.verify_otp({"phone": username, "token": str(sanitizedOtpCode), "type": 'sms'})
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

def determine_room_mouse_handler(e: MouseEventArguments):
    global isMasterBedroomLightsOn 
    global ismasterBathroomLightsOn

    areaFound = False

    for areaIndex in range(GC.MAX_AREA_INDEX_MASTER_BEDROOM):
        if GC.MASTER_BEDROOM_X[areaIndex] <= e.image_x <= GC.MASTER_BEDROOM_X[areaIndex] + GC.MASTER_BEDROOM_X_WIDTH[areaIndex] and \
           GC.MASTER_BEDROOM_Y[areaIndex] <= e.image_y <= GC.MASTER_BEDROOM_Y[areaIndex] + GC.MASTER_BEDROOM_Y_HEIGHT[areaIndex]:

            areaFound = True
            isMasterBedroomLightsOn = not isMasterBedroomLightsOn
            if isMasterBedroomLightsOn:
                ui.notify(message='Please wait turning Master Bedroom lights ON')
            else:
                ui.notify(message='Master Bedroom lights OFF')

            draw_light_highlight(ii, isMasterBedroomLightsOn, GC.MASTER_BEDROOM)
    
    for areaIndex in range(GC.MAX_AREA_INDEX_MASTER_BATHROOM):
        if GC.MASTER_BATHROOM_X[areaIndex] <= e.image_x <= GC.MASTER_BATHROOM_X[areaIndex] + GC.MASTER_BATHROOM_X_WIDTH[areaIndex] and \
           GC.MASTER_BATHROOM_Y[areaIndex] <= e.image_y <= GC.MASTER_BATHROOM_Y[areaIndex] + GC.MASTER_BATHROOM_Y_HEIGHT[areaIndex]:

            areaFound = True
            ismasterBathroomLightsOn = not ismasterBathroomLightsOn
            if ismasterBathroomLightsOn:
                ui.notify(message='Please wait turning Bathroom lights ON')
                
                # Telnet command
                telnet_command = f'(echo "enable" ; echo "configure" ; echo "interface \'0/{GC.MASTER_BATHROOM_SWITCH_PORT}\'" ; echo "poe opmode auto" ; echo "exit" ; echo "exit" ; echo "exit") | telnet localhost 23 ; exit;'
                stdin, stdout, stderr = ssh.exec_command(telnet_command)
                print(stdout.read().decode())
                
            else:
                ui.notify(message='Bathroom lights OFF')
                # Telnet command
                telnet_command = f'(echo "enable" ; echo "configure" ; echo "interface \'0/{GC.MASTER_BATHROOM_SWITCH_PORT}\'" ; echo "poe opmode shutdown" ; echo "exit" ; echo "exit" ; echo "exit") | telnet localhost 23 ; exit;'

                # Execute the command
                stdin, stdout, stderr = ssh.exec_command(telnet_command)
                output = stdout.read().decode()
                print(output)

            draw_light_highlight(ii, ismasterBathroomLightsOn, GC.MASTER_BATHROOM)
    
    if not areaFound:
        print("Clicked outside Master Bedroom and Bathroom areas")
        ui.notify(f'{e.type} at ({e.image_x:.1f}, {e.image_y:.1f})')

    
def draw_light_highlight(ii, isLightOn, roomName):
    global liteHouseLightState
    global lustronLightState

    print("Light State BEFORE change:", bin(liteHouseLightState))

    # Define the light state modifications for each room
    roomLightModificationsDict = {
        GC.MASTER_BEDROOM: (0b0000_0001, 0b1111_1110),
        GC.MASTER_BATHROOM: (0b0000_0010, 0b1111_1101),
        GC.BATHROOM_2: (0b0000_0011, 0b1111_1100),
        GC.BEDROOM_2: (0b0000_0100, 0b1111_1011),
        GC.BEDROOM_3: (0b0000_0101, 0b1111_1010),
        # Add more rooms and their corresponding modifications as needed
    }

    if roomName in roomLightModificationsDict:
        light_on_mask, light_off_mask = roomLightModificationsDict[roomName]
        if isLightOn:
            liteHouseLightState |= light_on_mask
        else:
            liteHouseLightState &= light_off_mask

    print("Light State AFTER change:", bin(liteHouseLightState))

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
        print('INVALID HOUSE TYPE')
        

def draw_signin_with_google_button():
    pass

def draw_signin_with_apple_button():
    #https://developer.apple.com/documentation/sign_in_with_apple/displaying_sign_in_with_apple_buttons_on_the_webn
    pass





if __name__ in {"__main__", "__mp_main__"}:

    # Run non GUI code that doesn't nee multiprocessor just once
    if __name__ == "__main__":
        
        darkMode.disable()
        #serveApp = PageKiteStartUp(homeName)

        db1 = HouseDatabase()

        apiRequest = requests.get(API.API_URL, timeout=2000)  # Timeout after 2000 milliseconds
        if apiRequest.status_code != 200:
            print(f'ERROR: Connection to API failed with code: {apiRequest.status_code}')
        else:
            print(f'API connection is OK: {apiRequest.json}')
        
        config = dotenv_values()
        url = config['SUPABASE_URL']
        key = config['SUPABASE_KEY']
        supabase: Client = create_client(url, key)
        print("IN NON-MULTIPROCESSOR MAIN")
    
        # Establish SSH connection with UniFi PoE Ethernet Switch
        if GC.SWITH_HARDWARE_CONNECTED:
            unifiSshUserName = config['USERNAME_UNIFI_USW_ENTERPRISE_24_POE']
            unifiSshpw = config['PASSWORD_UNIFI_USW_ENTERPRISE_24_POE']

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect('192.168.3.2', username=unifiSshUserName, password=unifiSshpw)

        ui.colors(primary=GC.MAMMOTH_BRIGHT_GRREN)
        
        pageKite = PageKiteAPI('litehouse.pagekite.me', config)
    
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
                ii = ui.interactive_image(houseType, on_mouse=determine_room_mouse_handler, events=['mousedown'], cross=True)
                
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
