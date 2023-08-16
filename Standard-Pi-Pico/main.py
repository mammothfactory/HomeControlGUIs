from SwitchClient import *
from NetworkConfig import *

DEBUG_STATMENTS_ON = True

if __name__ == "__main__":
    print("Starting main.py ")

    app = SwitchClient()
    
    app.debug_led_blink()
    
    print("Attempt to connect to the Wifi")
    wifiObject = NetworkConfig()
    
    while True:
        app.set_brightness(OFF)
        time.sleep(5)
        app.set_brightness(LOW)
        time.sleep(5)
        app.set_brightness(MEDIUM)
        time.sleep(5)
        app.set_brightness(HIGH)
        time.sleep(5)
        
    #r = urequests.get("https://google.com")
    #print(r.content)
    
    #sync_remote_switch(SWITCH_SN)
    
    #update_app(LOW, LOW, ON)
