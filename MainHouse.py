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


isDarkModeOn = False 
RUN_ON_NATIVE_OS = False
TUNNEL_TO_INTERNET = True

MAMMOTH_BRIGHT_GRREN = '#03C04A'       #'background-color: #03C04A'

tabNames = ['Lights', 'Cameras', 'Doors', 'Network']

# necessary until we improve native support for tabs (https://github.com/zauberzeug/nicegui/issues/251)


def switch_tab(msg: Dict) -> None:
    name = msg['args']
    tabs.props(f'model-value={name}')
    panels.props(f'model-value={name}')
    

def mouse_handler(e: MouseEventArguments):
    masterBedroomLightsOn = True
    if(e.image_x < 100):
        ui.notify(message='Turning Master Bedroom lights on')
        #ui.notify(f'{e.type} at ({e.image_x:.1f}, {e.image_y:.1f})')


if __name__ in {"__main__", "__mp_main__"}:
    darkMode = ui.dark_mode()
    darkMode.enable()
    homeName = 'My Casa'
    
    ui.colors(primary=MAMMOTH_BRIGHT_GRREN)
    
    src = 'https://github.com/mammothfactory/LitehouseGUIs/blob/7eb96631ffe8d0517fca93f381ffaab5750004dd/LiteHouseTopViewDrawing.jpeg?raw=true' #https://picsum.photos/id/565/640/360'
    
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

        
    with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
        infoButton = ui.button(on_click=footer.toggle).props('fab icon=info')


    # the page content consists of multiple tab panels
    with ui.element('q-tab-panels').props('model-value=A animated').classes('w-full') as panels:
        #for name in tabNames:
        with ui.element('q-tab-panel').props(f'name={tabNames[0]}').classes('w-full'):
            ui.label(f'Content of {name}')
            ii = ui.interactive_image(src, on_mouse=mouse_handler, events=['mousedown'], cross=True)   #events=['mousedown', 'mouseup']

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