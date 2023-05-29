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


from nicegui import app, ui
from typing import Dict
from datetime import datetime

from nicegui.events import MouseEventArguments

#import cv2


isDarkModeOn = False 
RUN_ON_NATIVE_OS = False
TUNNEL_TO_INTERNET = True

MASTER_BEDROOM_X = [1770]           # X pixel location of upper left corner
MASTER_BEDROOM_Y = [245]
MASTER_BEDROOM_X_WIDTH = [505]   
MASTER_BEDROOM_Y_HEIGHT = [580]
MASTER_BEDROOM = [MASTER_BEDROOM_X, MASTER_BEDROOM_Y, MASTER_BEDROOM_X_WIDTH, MASTER_BEDROOM_Y_HEIGHT]
masterBedroomLightsOn = True

BATHROOM_X = [1365]           # X pixel location of upper left corner
BATHROOM_Y = [410]
BATHROOM_X_WIDTH = [368]   
BATHROOM_Y_HEIGHT = [392]
bathroomLightsOn = True

MAMMOTH_BRIGHT_GRREN = '#03C04A'       #'background-color: #03C04A'

tabNames = ['lights', 'cameras', 'doors', 'network']
app.add_static_files('/static/images', 'static/images')

# necessary until we improve native support for tabs (https://github.com/zauberzeug/nicegui/issues/251)


def toggle_dark_mode():
    global isDarkModeOn
    if isDarkModeOn:
        darkMode.disable()
        isDarkModeOn = not isDarkModeOn 
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
    
    for areaIndex in range(len(MASTER_BEDROOM_X)):    
        if MASTER_BEDROOM_X[areaIndex] <= e.image_x <= MASTER_BEDROOM_X[areaIndex] + MASTER_BEDROOM_X_WIDTH[areaIndex] and \
           MASTER_BEDROOM_Y[areaIndex] <= e.image_y <= MASTER_BEDROOM_Y[areaIndex] + MASTER_BEDROOM_Y_HEIGHT[areaIndex]:
            
            
            masterBedroomLightsOn = not masterBedroomLightsOn
            if masterBedroomLightsOn:
                ui.notify(message='Turning Master Bedroom lights ON')
            else:
                ui.notify(message='Turning Master Bedroom lights OFF')
            
            draw_light_highlight(e.image_x, e.image_y,masterBedroomLightsOn)
            
        elif BATHROOM_X[areaIndex] <= e.image_x <= BATHROOM_X[areaIndex] + BATHROOM_X_WIDTH[areaIndex] and \
           BATHROOM_Y[areaIndex] <= e.image_y <= BATHROOM_Y[areaIndex] + BATHROOM_Y_HEIGHT[areaIndex]:
            
            bathroomLightsOn = not bathroomLightsOn
            if bathroomLightsOn:
                ui.notify(message='Turning Bathroom lights ON')
            else:
                ui.notify(message='Turning Bathroom lights OFF')
            
            draw_light_highlight(e.image_x, e.image_y, bathroomLightsOn)
            
        else:
            print("Clicked outside Master Bedroom and Bathroom areas")
            ui.notify(f'{e.type} at ({e.image_x:.1f}, {e.image_y:.1f})')

""""""
def draw_light_highlight(xPos, yPos):

    ui.html(f'''
            <svg viewBox="0 0 960 638" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <circle cx="{xPos}" cy="{yPos}" r="100" fill="yellow" stroke="red" stroke-width="20" />
            </svg>
    ''').classes('bg-transparent')
""""""
if __name__ in {"__main__", "__mp_main__"}:
    darkMode = ui.dark_mode()
    darkMode.disable()
    homeName = 'My Casa'
    
    ui.colors(primary=MAMMOTH_BRIGHT_GRREN)
    
    
    src = 'https://i.ibb.co/gWVGjpn/Lite-House-Top-View-Drawing.jpg' #'https://github.com/mammothfactory/LitehouseGUIs/blob/392ca21d544c76b8f7531d509c9d13deb153e016/LiteHouseTopViewDrawing-2.jpeg?raw=true' #https://picsum.photos/id/565/640/360'
    
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
            ui.label("407 E Central Blvd, Orlando, FL 32801")
 
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