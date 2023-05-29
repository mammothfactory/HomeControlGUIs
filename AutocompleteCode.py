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


from nicegui import ui
from typing import Dict
from datetime import datetime

from nicegui.events import MouseEventArguments

import csv

isDarkModeOn = False 
RUN_ON_NATIVE_OS = False
TUNNEL_TO_INTERNET = True

GENTEX_BLUE = '#0066CC'

tabNames = ['Requirements', 'Acronyms', 'CT+']

# necessary until we improve native support for tabs (https://github.com/zauberzeug/nicegui/issues/251)

def toggle_dark_mode():
    global isDarkModeOn
    if isDarkModeOn:
        darkMode.disable()
        isDarkModeOn = not isDarkModeOn 
    else:
        darkMode.enable()
        isDarkModeOn = not isDarkModeOn 

def csv_to_List(col, csv_file='/Users/mars/GentexDoorsAutomation/King_Requirement_App/AcronymDatabase.csv'):
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
    

def mouse_handler(e: MouseEventArguments):
    color = 'SkyBlue' if e.type == 'mousedown' else 'SteelBlue'
    masterBedroomLightsOn = True
    ii.content += f'<circle cx="{e.image_x}" cy="{e.image_y}" r="15" fill="none" stroke="{color}" stroke-width="4" />'
    if(e.image_x < 100):
        ui.notify('Turning Master Bedroom lights on')
        #ui.notify(f'{e.type} at ({e.image_x:.1f}, {e.image_y:.1f})')


if __name__ in {"__main__", "__mp_main__"}:
    darkMode = ui.dark_mode()
    darkMode.disable()
    
    ui.colors(primary=GENTEX_BLUE)
    
    src = 'https://picsum.photos/id/565/640/360' #'https://github.com/OpenSourceIronman/Automation/blob/main/King_Requirement_App/LiteHouseTopViewDrawing.jpeg'

    
    with ui.header().classes(replace='row items-center') as header:
        ui.button(on_click=lambda: left_drawer.toggle()).props('flat color=white icon=settings')
        with ui.element('q-tabs').on('update:model-value', switch_tab) as tabs:
            for name in tabNames:
                ui.element('q-tab').props(f'name={name} label={name}')

    with ui.footer(value=False) as footer:
        ui.label('Send bug reports to blaze.sanders@gentex.com')

    with ui.left_drawer().classes('bg-white-100') as left_drawer:
        
        with ui.grid(columns=1):
            darkModeSwitch = ui.switch('Enable Dark Mode', on_change=toggle_dark_mode)

        
    with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
        infoButton = ui.button(on_click=footer.toggle).props('fab icon=bug_report')

    acronymList = csv_to_List(0)
    fullnameList = csv_to_List(1)
    
    # the page content consists of multiple tab panels
    with ui.element('q-tab-panels').props('model-value=A animated').classes('w-full') as panels:

        with ui.element('q-tab-panel').props(f'name={tabNames[0]}').classes('w-full'):
            ui.label(f'Content of {name}')
            ii = ui.interactive_image(src, on_mouse=mouse_handler, events=['mousedown', 'mouseup'], cross=True)
            
        with ui.element('q-tab-panel').props(f'name={tabNames[1]}').classes('w-full'):
            with ui.grid(columns=1):
                ui.label("Found word is:")
                result = ui.label()
                
                try:
                    ui.input(label='Start typing', placeholder='start typing', \
                            on_change=lambda e: result.set_text(fullnameList[acronymList.index(e.value)]), \
                            autocomplete=acronymList,   
                            validation={'Input too long': lambda value: len(value) < 20})
                    
                    #fullnameIndex =  
                except not ValueError:
                    result = ui.label()
                

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
   