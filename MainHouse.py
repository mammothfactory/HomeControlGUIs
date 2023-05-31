#!/usr/bin/env python3
"""
__authors__    = ["Blaze Sanders"]
__contact__    = "blaze.d.a.sanders@gmail.com"
__copyright__  = "Copyright 2023"
__license__    = "GPLv3"
__status__     = "Development
__deprecated__ = False
__version__    = "0.0.1"
__doc__        = "Generate 3 page GUI to cross check requirements to lab test and find acronyms"
"""
# https://www.analyticsvidhya.com/blog/2023/05/elevate-your-python-apps-with-nicegui-the-ultimate-gui-framework/

from typing import Dict
from datetime import datetime

import GlobalConstants as GC

try:  # Importing externally developed libraries

    # Open source plaform for NoSQL databases, authentication, file storage, and auto-generated APIs
    # https://github.com/supabase-community/supabase-py
    from supabase import create_client, Client   #TODO REMOVE?, execute
    from nicegui import app, ui
    from nicegui.events import MouseEventArguments

except ImportError:
    print("ERROR: The supabase python module didn't import correctly!")
    executeInstalls = input("Would you like me to *** pip3 install supabase *** for you (Y/N)? ")
    if(executeInstalls.upper() == "Y" or executeInstalls.upper() == "YES"):
        check_call("sudo apt install python3-pip", shell=True)
        check_call("pip3 install supabase", shell=True)
    else:
        print("You didn't type Y or YES :)")
        print("Follow supabase manual install instructions at https://pypi.org/project/supabase/")


#import cv2

# Global Variables
isDarkModeOn = True
RUN_ON_NATIVE_OS = False
TUNNEL_TO_INTERNET = True

masterBedroomLightsOn = True
bathroomLightsOn = True
homeName = 'Casa'
homeAddress = '407 E Central Blvd, Orlando, FL 32801'
pageKiteURL = homeName + 'mammothlitehouse.pagekite.com'.  #TODO
tabNames = ['lights', 'cameras', 'doors', 'network']

# Create directory and URL for local storage of images
app.add_static_files('/static/images', 'static/images')
src = 'https://i.ibb.co/gWVGjpn/Lite-House-Top-View-Drawing.jpg' #'https://github.com/mammothfactory/LitehouseGUIs/blob/392ca21d544c76b8f7531d509c9d13deb153e016/LiteHouseTopViewDrawing-2.jpeg?raw=true' #https://picsum.photos/id/565/640/360'
    
# necessary until we improve native support for tabs (https://github.com/zauberzeug/nicegui/issues/251)

def toggle_dark_mode():
    global isDarkModeOn
    
    if isDarkModeOn:
        darkMode.disable(): 
    else:
        darkMode.enable()
        
    isDarkModeOn = not isDarkModeOn 

def switch_tab(msg: Dict) -> None:
    name = msg['args']
    tabs.props(f'model-value={name}')
    panels.props(f'model-value={name}')
    
def mouse_handler(e: MouseEventArguments):
    global masterBedroomLightsOn 
    global bathroomLightsOn 
    
    for areaIndex in range(ROOM_DEFINITION)):    
        if GC.MASTER_BEDROOM_X[areaIndex] <= e.image_x <= GC.MASTER_BEDROOM_X[areaIndex] + GC.MASTER_BEDROOM_X_WIDTH[areaIndex] and \
           GC.MASTER_BEDROOM_Y[areaIndex] <= e.image_y <= GC.MASTER_BEDROOM_Y[areaIndex] + GC.MASTER_BEDROOM_Y_HEIGHT[areaIndex]:
            
            
            masterBedroomLightsOn = not masterBedroomLightsOn
            if masterBedroomLightsOn:
                ui.notify(message='Turning Master Bedroom lights ON')
            else:
                ui.notify(message='Turning Master Bedroom lights OFF')
            
            draw_light_highlight(e.image_x, e.image_y, masterBedroomLightsOn)
            
        elif GC.MASTER_BATHROOM_X[areaIndex] <= e.image_x <= GC.MASTER_BATHROOM_X[areaIndex] + GC.MASTER_BATHROOM_X_WIDTH[areaIndex] and \
           GC.MASTER_BATHROOM_Y[areaIndex] <= e.image_y <= GC.MASTER_BATHROOM_Y[areaIndex] + GC.MASTER_BATHROOM_Y_HEIGHT[areaIndex]:
            
            bathroomLightsOn = not bathroomLightsOn
            if bathroomLightsOn:
                ui.notify(message='Turning Bathroom lights ON')
            else:
                ui.notify(message='Turning Bathroom lights OFF')
            
            draw_light_highlight(e.image_x, e.image_y, bathroomLightsOn, MASTER_BATHROOM)
            
        else:
            print("Clicked outside Master Bedroom and Bathroom areas")
            ui.notify(f'{e.type} at ({e.image_x:.1f}, {e.image_y:.1f})')

""""""
def draw_light_highlight(xPos, yPos, roomName):

    if roomName == MASTER_BEDROOM:
        pass
    elif roomName == MASTER_BATHROOM:
        pass
    ui.html(f'''
            <svg viewBox="0 0 960 638" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <circle cx="{xPos}" cy="{yPos}" r="100" fill="yellow" stroke="red" stroke-width="20" />
            </svg>
    ''').classes('bg-transparent')
""""""

if __name__ in {"__main__", "__mp_main__"}:
    darkMode = ui.dark_mode()
    darkMode.enable()
    
    ui.colors(primary=GC.MAMMOTH_BRIGHT_GRREN)
    
    with ui.header().classes(replace='row items-center') as header:
        ui.button(on_click=lambda: left_drawer.toggle()).props('flat color=white icon=home')
        with ui.element('q-tabs').on('update:model-value', switch_tab) as tabs:
            for name in tabNames:
                ui.element('q-tab').props(f'name={name} label={name}')

    with ui.footer(value=False) as footer:
        ui.label('Mammoth Factory Corp')

    with ui.left_drawer().classes('bg-white-100') as left_drawer:
        
        with ui.grid(columns=2):
            ui.label('Home Name:').tailwind.font_weight('extrabold').text_color('green-900')
            ui.label(homeName).style('gap: 10px')
        
            ui.label('Home Address:').tailwind.font_weight('extrabold').text_color('green-900')
            ui.label(homeAddress)
 
            ui.label('Home GPS:').tailwind.font_weight('extrabold').text_color('green-900')
            ui.label("28.54250516114, -81.372488625")
        
        with ui.grid(columns=1):   
            darkModeSwitch = ui.switch('Enable Dark Mode', on_change=toggle_dark_mode)

        
    with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
        infoButton = ui.button(on_click=footer.toggle).props('fab icon=info')


    # the page content consists of multiple tab panels
    with ui.element('q-tab-panels').props('model-value=A animated').classes('w-full') as panels:
        #for name in tabNames:
        
        with ui.element('q-tab-panel').props(f'name={tabNames[0]}').classes('w-full'):
            with ui.grid(columns=1):
                ui.label(f'Click on image to toggle {tabNames[0]}').tailwind('mx-auto text-2xl')
                ii = ui.interactive_image(src, on_mouse=mouse_handler, events=['mousedown'], cross=True)  #events=['mousedown', 'mouseup']
                
        with ui.element('q-tab-panel').props(f'name={tabNames[1]}').classes('w-full'):
            with ui.grid(columns=1):
                ui.image('https://picsum.photos/id/377/640/360')
                
        with ui.element('q-tab-panel').props(f'name={tabNames[2]}').classes('w-full'):
            with ui.grid(columns=1):        
                ui.image('static/images/doorOpening.gif')
                        
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