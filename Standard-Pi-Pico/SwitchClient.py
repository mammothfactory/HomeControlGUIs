from machine import Pin, PWM
import machine
import urequests
import math
import time



# Prime number above 1000 Hz so flicker not visible tp human or modulus 30 or 60 for camera flicker
NON_FLICKER_FREQ = 1013

# https://www.reddit.com/r/raspberrypipico/comments/wqr3i9/control_mosfet_module_output_via_pico_pwm_signal/
# https://docs.micropython.org/en/latest/library/machine.Pin.html?highlight=pin#machine.Pin.drive
HIGH_POWER_FREQ = 10 

# Discrete LED brightness levels to 4 significant digits
OFF = 0.000
LOW = 33.33
MEDIUM = 66.66
HIGH = 100.0

ON_BOARD_LED = 25

MAX_DUTY_CYCLE = 65535

CLOSET_LIGHT_TIMEOUT = 30 # Units = Seconds

#https://forums.raspberrypi.com/viewtopic.php?t=313072#:~:text=The%20bottom%20line%20is%20that,have%20access%20to%20the%20software.
SWITCH_SN = 001   # TODO Change this to MAC address if all the Pi Pico have different values

class SwitchClient:

    def __init__(self):
        print("Initializing SwitchController.py using microPython on a Pi Pico")
        
        # Pin(0) = GP0 = PWM_A[0], Pin(1) = GP1 = PWM_B[0], Pin(6) = GP6 = PWM_A[3], Pin(7) = GP7 = PWM_B[3]
        # Can't set drive parameter on Pi Pico micropython https://docs.micropython.org/en/latest/library/machine.Pin.html#machine.Pin.drive
        self.lightD = PWM(Pin(0, Pin.OUT, Pin.PULL_DOWN), HIGH_POWER_FREQ)
        self.lightC = PWM(Pin(1, Pin.OUT, Pin.PULL_DOWN), HIGH_POWER_FREQ)
        self.lightB = PWM(Pin(6, Pin.OUT, Pin.PULL_DOWN), HIGH_POWER_FREQ)
        self.lightA = PWM(Pin(7, Pin.OUT, Pin.PULL_DOWN), HIGH_POWER_FREQ)

        # On-Board LED drive from the wifi IC
        self.debugLED = machine.Pin("LED", machine.Pin.OUT)
  

    def debug_led_blink(self):
        self.debugLED.on()
        time.sleep(1)
        self.debugLED.off()


    def set_fan_speed(self, value: float):
        print(f'Set fan speed to: {value}%')


    def set_brightness(self, value: float):
        """ Set all four light levels defined by PWM resolution 2^16 for ranges between 0 to 65535
        """
        dutyCycle = int((value/100.0)*MAX_DUTY_CYCLE)
        print(f'Setting all 4 lights to {value}% brightness')
        self.lightA.duty_u16(dutyCycle)
        self.lightB.duty_u16(dutyCycle)
        self.lightC.duty_u16(dutyCycle)
        self.lightD.duty_u16(dutyCycle)
        ##REMOVE?time.sleep(1/NON_FLICKER_FREQ)
        

    def update_app(self, lightBrightness, fanSpeed, louverState):
        """ PUT data into server running FastAPI on ZimaBoard using HouseAPI.py 
        """
        request = urequests.put(FAST_API_URL, data={'switchId':SWITCH_SN})
        if request != SUCCESS_CODE:
            print("ERROR: FAST API not updated")
        
        #print(request.content)
            
            
    def sync_remote_switch(self, switchControllerId):
        """" GET data from webserver running FastAPI on ZimaBoard using HouseAPI.py  
        """
        request = urequests.get(FAST_API_URL)
        print(request)     #print(request.content)


    def auto_ligth_shutdown(self, switchControllerId, timeout=CLOSET_LIGHT_TIMEOUT):
        pass


        
if __name__ == "__main__":
    print("Starting SwitchClient Main()")
    app = SwitchClient()
    
    app.debug_led_blink()
    
    while True:
        app.set_brightness(OFF)
        time.sleep(3)
        app.set_brightness(HIGH)
        time.sleep(3)





    




