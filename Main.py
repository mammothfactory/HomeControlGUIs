from nicegui import ui
from datetime import datetime

isDarkModeOn = False
RUN_ON_NATIVE_OS = True
TUNNEL_TO_INTERNET = True


def toggle_dark_mode():
    global isDarkModeOn
    if isDarkModeOn:
        darkMode.disable()
        isDarkModeOn = not isDarkModeOn 
    else:
        darkMode.enable()
        isDarkModeOn = not isDarkModeOn 

def find_system_name(text):
    if text.upper() == 'L':
        return "Lights" 
    else:
        return text

if __name__ in {"__main__", "__mp_main__"}:
    darkMode = ui.dark_mode()
    darkMode.disable()
    
    with ui.grid(columns=2): #.FlexContainer(style={'height': '100vh', 'justify-content': 'center', 'align-items': 'center'}):
       darkModeSwitch = ui.switch('Enable Dark Mode', on_change=toggle_dark_mode)
       timerLabel = ui.label()

       ui.timer(1.0, lambda: timerLabel.set_text(f'{datetime.now():%X}'))

       ui.icon('home', color='red').classes('text-5xl')
       ui.icon('search', color='blue').classes('text-5xl') #, flex items-center h-screen, mx-auto')
    
       ui.input(label='System', placeholder='', \
                on_change=lambda e: result.set_text(find_system_name(e.value)), \
                validation={'Input too long': lambda value: len(value) < 20})

       result = ui.label()

       ui.color_input(label='Color', value='#000000', \
                      on_change=lambda e: label.style(f'color:{e.value}'))

       with ui.button('Click to check door bell camera recordings', on_click=lambda: badge.set_text(int(badge.text) + 1)):
           badge = ui.badge('0', color='red').props('floating')


    if TUNNEL_TO_INTERNET:
        # Use http://localhost.run
        ui.run(native=False)
    else:
        ui.run(native=RUN_ON_NATIVE_OS)

