from nicegui import ui
from datetime import datetime


darkMode = ui.dark_mode()
darkMode.disable()
isDarkModeOn = False


def toggle_dark_mode():
    global isDarkModeOn
    if isDarkModeOn:
        darkMode.disable()
        isDarkModeOn = not isDarkModeOn 
        darkModeSwitch.style() #Set to defult system color
    else:
        darkMode.enable()
        isDarkModeOn = not isDarkModeOn 
        darkModeSwitch.style('color: #FF0000')

def findSystemName(text):
    if text.upper() == 'L':
        return "Lights" 
    else:
        return text

if __name__ in {"__main__", "__mp_main__"}:

    with ui.grid(columns=2):
        darkModeSwitch = ui.switch('Enable Dark Mode', on_change=toggle_dark_mode).style('color: #FF0000')
        timerLabel = ui.label()

        ui.timer(1.0, lambda: timerLabel.set_text(f'{datetime.now():%X}'))

        ui.icon('home', color='red').classes('text-5xl')
        ui.icon('search', color='blue').classes('text-5xl, w-100')
    
        ui.input(label='System', placeholder='', \
                 on_change=lambda e: result.set_text(findSystemName(e.value)), \
                 validation={'Input too long': lambda value: len(value) < 20})

    result = ui.label()

    ui.run(native=True)
