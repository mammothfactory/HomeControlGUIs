#!/usr/bin/env python3
"""
__authors__    = ["Blaze Sanders"]
__contact__    = "blaze.d.a.sanders@gmail.com"
__copyright__  = "Copyright 2023"
__license__    = "GPLv3"
__status__     = "Development
__deprecated__ = False
__version__    = "0.0.1"
__doc__        = "Generate a tab based GUI to control LiteHouse and Lustron house styles"
"""
# https://www.analyticsvidhya.com/blog/2023/05/elevate-your-python-apps-with-nicegui-the-ultimate-gui-framework/

from typing import Dict

from nicegui import app, ui
from nicegui.events import MouseEventArguments

from datetime import datetime
import subprocess
from dotenv import dotenv_values

from PageKiteStartUp import *
import GlobalConstants as GC

try:  # Importing externally developed libraries

    # Open source plaform for NoSQL databases, authentication, file storage, and auto-generated APIs
    # https://github.com/supabase-community/supabase-py
    #import supabase
    from supabase import create_client, Client   #TODO REMOVE?, execute


except ImportError:
    print("ERROR: The supabase python module didn't import correctly! ")
    executeInstalls = input("Would you like me to *** pip3 install supabase *** for you (Y/N)? ")
    if(executeInstalls.upper() == "Y" or executeInstalls.upper() == "YES"):
        subprocess.call(['sudo', 'apt', 'install', 'python3-pip'])
        subprocess.call(['pip3', 'install', 'supabase',])
    else:
        print("You didn't type Y or YES :)")
        print("Follow supabase manual install instructions at https://pypi.org/project/supabase/")


#import cv2

# Global Variables
isDarkModeOn = False
userLoggedIn = False
darkMode = ui.dark_mode()
sanitizedPhoneNumber = '555555555'
RUN_ON_NATIVE_OS = False
TUNNEL_TO_INTERNET = True

masterBedroomLightsOn = False
bathroomLightsOn = False
houseType = GC.LITEHOUSE
liteHouseLightState = 0b0000_0000
lustronLightState = 0b0000_0000
homeName = 'mammothlitehouse'
homeAddress = '407 E Central Blvd, Orlando, FL 32801'
pageKiteURL = homeName + 'mammothlitehouse.pagekite.com'  #TODO
tabNames = ['lights', 'cameras', 'doors', 'network']

# Create directory and URL for local storage of images
app.add_static_files('/static/images', 'static/images')
#app.add_static_files('/static/vidoes', 'static/videos')
liteHouseSource = 'https://i.ibb.co/gWVGjpn/Lite-House-Top-View-Drawing.jpg' #'https://github.com/mammothfactory/LitehouseGUIs/blob/392ca21d544c76b8f7531d509c9d13deb153e016/LiteHouseTopViewDrawing-2.jpeg?raw=true' #https://picsum.photos/id/565/640/360'
liteHouseSource0000_0001 = 'static/images/TODO.jpg'
liteHouseSource0000_0010 = 'static/images/TODO.jpg'
liteHouseSource0000_0011 = 'static/images/TODO.jpg'
liteHouseSource0000_0100 = 'static/images/TODO.jpg'
liteHouseSource0000_0101 = 'static/images/TODO.jpg'
liteHouseSource0000_0110 = 'static/images/TODO.jpg'
liteHouseSource0000_0111 = 'static/images/TODO.jpg'

# necessary until we improve native support for tabs (https://github.com/zauberzeug/nicegui/issues/251)

def toggle_dark_mode():
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
    
def attempt_phone_login(phoneNumber, invalidPhoneNumberLabel, signInGrid):
    # TODO Connect to supabase
    if phoneNumber == '7196390839' or phoneNumber == '5303668296': 
        userFound = True  
    else:
        userFound = False  
        
    if not userFound:
        invalidPhoneNumberLabel.set_text(phoneNumber + ' not found, create an account')
        invalidPhoneNumberLabel.tailwind.font_weight('extrabold').text_color('red-600')
        invalidPhoneNumberLabel.visible = True
    else:
        userDataForm.visible = True
        signInGrid.visible = False
        
def reset_login_gui(invalidPhoneNumberLabel, signInGrid, userDataForm):
    invalidPhoneNumberLabel.visible = False
    signInGrid.visible = True
    userDataForm.visible = False
    
def csv_to_List(col, csv_file=GC.HOME_DIRECTORY+'TODO.csv'):
    result = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            result.append(row[col])  # Append only the first column
    return result

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
    
    print(sanitizedPhoneNumber)
    
    return sanitizedPhoneNumber

def determine_room_mouse_handler(e: MouseEventArguments):
    global masterBedroomLightsOn 
    global bathroomLightsOn 
    
    areaFound = False

    for areaIndex in range(GC.MAX_AREA_INDEX_MASTER_BEDROOM):    
        if GC.MASTER_BEDROOM_X[areaIndex] <= e.image_x <= GC.MASTER_BEDROOM_X[areaIndex] + GC.MASTER_BEDROOM_X_WIDTH[areaIndex] and \
           GC.MASTER_BEDROOM_Y[areaIndex] <= e.image_y <= GC.MASTER_BEDROOM_Y[areaIndex] + GC.MASTER_BEDROOM_Y_HEIGHT[areaIndex]:
            
            areaFound = True
            masterBedroomLightsOn = not masterBedroomLightsOn
            if masterBedroomLightsOn:
                ui.notify(message='Turning Master Bedroom lights ON')
            else:
                ui.notify(message='Turning Master Bedroom lights OFF')
    
            draw_light_highlightBETTER(ii, masterBedroomLightsOn, GC.MASTER_BEDROOM)
    
    maxAreaIndex = int(len(GC.MASTER_BATHROOM_RECT_AREAS)/GC.ROOM_DEFINITION)
    for areaIndex in range(GC.MAX_AREA_INDEX_MASTER_BATHROOM):         
        if GC.MASTER_BATHROOM_X[areaIndex] <= e.image_x <= GC.MASTER_BATHROOM_X[areaIndex] + GC.MASTER_BATHROOM_X_WIDTH[areaIndex] and \
           GC.MASTER_BATHROOM_Y[areaIndex] <= e.image_y <= GC.MASTER_BATHROOM_Y[areaIndex] + GC.MASTER_BATHROOM_Y_HEIGHT[areaIndex]:
            
            areaFound = True
            bathroomLightsOn = not bathroomLightsOn
            if bathroomLightsOn:
                ui.notify(message='Turning Bathroom lights ON')
            else:
                ui.notify(message='Turning Bathroom lights OFF')
            
            draw_light_highlightBETTER(ii, bathroomLightsOn, GC.MASTER_BATHROOM)
    
    if not areaFound:   
        print("Clicked outside Master Bedroom and Bathroom areas")
        ui.notify(f'{e.type} at ({e.image_x:.1f}, {e.image_y:.1f})')


def draw_light_highlight(ii, islighOn, roomName):
    
    global liteHouseLightState
    print("Light State BEFORE change: " + str(liteHouseLightState))
    
    if roomName == GC.MASTER_BEDROOM:
        if(islighOn):
            liteHouseLightState = liteHouseLightState | 0b0000_0001
        else:
            liteHouseLightState = liteHouseLightState & 0b1111_1110
        
    elif roomName == GC.MASTER_BATHROOM:
        pass

    print("Light State AFTER change: " + str(liteHouseLightState))
    if liteHouseLightState == 0b0000_0001:
        pass
        #ii.set_source(masterBedroomOnSource) 
    
    ui.update(ii)
    
    
def draw_light_highlightBETTER(ii, isLightOn, roomName):
    global liteHouseLightState
    global lustronLightState
    
    print("Light State BEFORE change:", bin(liteHouseLightState))

    # Define the light state modifications for each room
    roomLightModificationsDict = {
        GC.MASTER_BEDROOM: (0b0000_0001, 0b1111_1110),
        GC.MASTER_BATHROOM: (0b0000_0010, 0b1111_1101)
        #GC.BEDROOM_2: (0b0000_0100, 0b1111_1011),
        # Add more rooms and their corresponding modifications as needed
    }

    if roomName in roomLightModificationsDict:
        light_on_mask, light_off_mask = roomLightModificationsDict[roomName]
        if isLightOn:
            liteHouseLightState |= light_on_mask
        else:
            liteHouseLightState &= light_off_mask

    print("Light State AFTER change:", bin(liteHouseLightState))

    if houseType == GC.LITEHOUSE:
        if liteHouseLightState == 0b0000_0000:
            ii.set_source(liteHouseSource)
        elif liteHouseLightState == 0b0000_0001:
            ii.set_source(liteHouseSource0000_0001)
        elif liteHouseLightState == 0b0000_0010:
            ii.set_source(liteHouseSource0000_0010)
        elif liteHouseLightState == 0b0000_0011:
            ii.set_source(liteHouseSource0000_0011)
        elif liteHouseLightState == 0b0000_0100:
            ii.set_source(liteHouseSource0000_0100)
        elif liteHouseLightState == 0b0000_0101:
            ii.set_source(liteHouseSource0000_0101)
        elif liteHouseLightState == 0b0000_0110:
            ii.set_source(liteHouseSource0000_0110)
        elif liteHouseLightState == 0b0000_0111:
            ii.set_source(liteHouseSource0000_0111)
    
    elif houseType == GC.LUSTRON:
        if lustronLightState == 0b0000_0001:
            pass
    else:
        print('INVALID HOUSE TYPE')
        
    ui.update(ii)


def draw_signin_with_google_button():
    pass

def draw_signin_with_apple_button():
    #https://developer.apple.com/documentation/sign_in_with_apple/displaying_sign_in_with_apple_buttons_on_the_webn
    pass

if __name__ in {"__main__", "__mp_main__"}:
    darkMode.disable()
    #serveApp = PageKiteStartUp(homeName)
    
    environmentVariables = dotenv_values()
    url = environmentVariables['SUPABASE_URL']
    key = environmentVariables['SUPABASE_KEY']
    supabase: Client = create_client(url, key)

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
            
            signInGrid = ui.grid(columns=1)
            with signInGrid:
                
                invalidPhoneNumberLabel = ui.label()
                invalidPhoneNumberLabel.visible = False
                ui.input(label='Enter your 10 digit phone number', placeholder='e.g. 7195551234', \
                                on_change=lambda e: invalidPhoneNumberLabel.set_text(sanitize_phone_number(e.value)), \
                                validation={'Phone number is too long': lambda value: len(sanitizedPhoneNumber) <= GC.VALID_USA_CANADA_MEXICO_PHONE_NUMBER_LENGTH})  # Length incluses + symbol at start of phone number
                
                signInButton = ui.button('SIGN IN', on_click=lambda e: attempt_phone_login(sanitizedPhoneNumber, invalidPhoneNumberLabel, signInGrid))
                
                #draw_signin_with_apple_button()
                #draw_signin_with_google_button()

                ui.label('')
                ui.label('')

        userDataForm = ui.grid(columns=2)
        userDataForm.visible = False
        with userDataForm:
            ui.label('Home Name:').tailwind.font_weight('extrabold')
            ui.label(homeName).style('gap: 10px')
        
            ui.label('Home Address:').tailwind.font_weight('extrabold')
            ui.label(homeAddress)

            ui.label('Home GPS:').tailwind.font_weight('extrabold')
            ui.label("28.54250516114, -81.372488625")
            
            signOutButton = ui.button('SIGN OUT', on_click=lambda e: reset_login_gui(invalidPhoneNumberLabel, signInGrid, userDataForm))
        


        
    with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
        infoButton = ui.button(on_click=footer.toggle).props('fab icon=info')

    
    # the page content consists of multiple tab panels
    with ui.element('q-tab-panels').props('model-value=A animated').classes('w-full') as panels:
        #for name in tabNames:
        
       
        with ui.element('q-tab-panel').props(f'name={tabNames[0]}').classes('w-full'):
            with ui.grid(columns=1):
                ui.label(f'Click on image to toggle {tabNames[0]}').tailwind('mx-auto text-2xl')
                ii = ui.interactive_image(liteHouseSource, on_mouse=determine_room_mouse_handler, events=['mousedown'], cross=True)
                
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
                ui.mermaid('''
                graph LR;
                    A[UniFi PoE Switch] --> B[ROOM: Master Bedroom];
                    A[UniFi PoE Switch] --> F[ZimaBoard Server]
                    F[CPU: ZimaBoard Server] --> E[DISPLAY: Main Central Control];
                    B[ROOM: Master Bedroom] --> C[LIGHT: Master Bedroom]; 
                    B[ROOM: Master Bedroom] --> D[DISPLAY: Master Bedroom];
                    A[UniFi PoE Switch] --> LIGHT-Kitcen;
                    
                    style A color:#000000, fill:#03C04A, stroke:#000000
                    style B color:#000000, fill:#03COFF, stroke:#000000
                    style C color:#000000, fill:#FFC04A, stroke:#000000
                    style D color:#FFFFFF, fill:#1F1F1F, stroke:#000000
                    style E color:#FFFFFF, fill:#1F1F1F, stroke:#000000
                    style F color:#000000, fill:#B8191D, stroke:#000000
                ''')
    ui.run(native=RUN_ON_NATIVE_OS)

    """
    ui.label('Select Input Source').classes('m-auto justify-center')
    
    ui.date(value=datetime.now(), on_change=lambda e: result.set_text(e.value)).classes('m-auto justify-center')
    result = ui.label()
    
    iso8601date = datetime.now()
    
    
                
    with ui.row():
        ui.label('Enter DOORS Requirement ID:').classes('text-3xl')    
        ui.input(label='e.g. HW-3778-5', placeholder='')
    """