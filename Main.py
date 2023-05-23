from nicegui import ui

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

darkModeSwitch = ui.switch('Enable Dark Mode', on_change=toggle_dark_mode).style('color: #FF0000')





def findSystemName(text):
    if text.upper() == 'L':
        return "Lights" 
    else:
        return text

with ui.grid(columns=2):
    ui.icon('home', color='red').classes('text-10xl')
    ui.icon('search', color='blue').classes('text-10xl')
    
    ui.input(label='System', placeholder='',
         on_change=lambda e: result.set_text(findSystemName(e.value)),
         validation={'Input too long': lambda value: len(value) < 20})

    result = ui.label()





ui.run(native=True)
