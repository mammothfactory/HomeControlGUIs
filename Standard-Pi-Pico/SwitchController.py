#Controllers
# https://forums.raspberrypi.com//viewtopic.php?f=37&t=124184

# https://picockpit.com/raspberry-pi/stream-sensor-data-over-wifi-with-raspberry-pi-pico-w/


# https://www.aliexpress.us/item/3256804994106850.html?aff_platform=true&aff_short_key=UneMJZVf&isdl=y&src=bing&pdp_npi=3%40dis%21USD%2113.76%2112.39%21%21%212.96%21%21%40%2112000033376521404%21ppc%21%21&albch=shopping&acnt=135095331&isdl=y&albcp=373871275&albag=1308419064071836&slnk=&trgt=pla-4585375808811125&plac=&crea=81776241344382&netw=o&device=c&mtctp=e&utm_source=Bing&utm_medium=shopping&utm_campaign=PA_Bing_customlabel1_US_PC&utm_content=customlabel1%3D7&utm_term=P%20iPico%20TOuch%20screen&msclkid=b8db1aa5e0ad1da132657e131795f3bd&gatewayAdapt=glo2usa
# https://www.amazon.com/12V-24V-Single-Controller-Dimmer-Brightness/dp/B01MTQSIG7/ref=asc_df_B01MTQSIG7/?tag=hyprod-20&linkCode=df0&hvadid=241980973821&hvpos=&hvnetw=g&hvrand=15885852254165248059&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9011640&hvtargid=pla-567804767262&th=1
# https://www.amazon.com/Wall-mounted-Dimmer-Switch-Brightness-Controller/dp/B07L3MT41G/ref=pd_bxgy_img_sccl_1/139-8951308-4939835?pd_rd_w=GUzMt&content-id=amzn1.sym.26a5c67f-1a30-486b-bb90-b523ad38d5a0&pf_rd_p=26a5c67f-1a30-486b-bb90-b523ad38d5a0&pf_rd_r=CWVB1K49ZAF1R45PEA5Z&pd_rd_wg=JEpGA&pd_rd_r=b19c3427-9237-4651-855b-c1339b7616b0&pd_rd_i=B07L3MT41G&th=1
# https://www.amazon.com/stores/page/4CDE47BE-84B7-46F6-AB85-13CC6D868DA4?ingress=0&visitId=f1f15a16-84a6-4121-a61b-009c456dd507&ref_=as_li_ss_tl
# https://www.tiktok.com/@levvenelectronics
# https://iottysmarthome.com/pages/technical
# https://moeshouse.com/products/us-zigbee-glass-touch-3-way-light-switch?variant=39797103231057&utm_source=google02&utm_medium=cpc&network=x&keyword=&campaignid=20331101469&gad=1&gclid=Cj0KCQjw8NilBhDOARIsAHzpbLCOGAFpJEkwFIaA0apU5OMHG9eeueIXlx7d8Sr8kw7ulh1h-UlmdzQaAn7QEALw_wcB

# Pi Pico SQLite Database
# https://pypi.org/project/micropython-sqlite3
# https://github.com/micropython/micropython-lib/blob/7128d423c2e7c0309ac17a1e6ba873b909b24fcc/unix-ffi/sqlite3/sqlite3.py
# https://forum.micropython.org/viewtopic.php?t=8213
# https://github.com/micropython/micropython-lib/pull/376


# https://sqlitebrowser.org/dl/

# https://www.spotpear.com/index/product/detail/id/1211.html
# https://www.spotpear.com/index/product/detail/id/1204.html

import HouseAPI as API

CLOSET_LIGHT_TIMEOUT = 360  # Seconds

class SwitchController:
    """ Display and 24V power controller for Pi Pico W and 
    """

    def __init__(self):
        """ https://github.com/pi3g/pico-w/tree/main/MicroPython
        """

        # Setup vlan backend only wifi via QR Code https://github.com/predmijat/qr_wifi


    def sync_remote_switch_to_app(self):
        """ Read from webserver running on Pi Pico 
        """
        pass

    def sync_app_to_remote_switch(self):
        """" GET from webserver running FastAPI on ZimaBoard using HouseAPI.py  
        """
        pass


    def auto_ligth_shutdown(self, switchControllerId, timeout=CLOSET_LIGHT_TIMEOUT):
        pass


# Network Config.py on Pi Pico
import rp2
import ubinascii
import urequests as requests
import network

# https://picockpit.com/raspberry-pi/everything-about-the-raspberry-pi-pico-w/

class NetworkConfig:
    
    def __init__(self):
        # Set country to avoid possible errors
        rp2.country('US')

        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        # If you need to disable powersaving mode
        # wlan.config(pm = 0xa11140)

        # See the MAC address in the wireless chip OTP
        mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
        print('MAC (Media Access Control) address = ' + mac)

        # Other things to query
        # print(wlan.config('channel'))
        # print(wlan.config('essid'))
        # print(wlan.config('txpower'))

        # Load login data from different file for safety reasons
        ssid = 'MFC Wifi'
        pw = 'Webuild3521#'

        wlan.connect(ssid, pw)



# SwitchClient.py on Pi Pico
from machine import Pin, PWM
import math
import time

from NetworkConfig import *


NON_FLICKER_FREQ = 1013		# Prime number above 1000 Hz so flicker not visible tp human or modulus 30 or 60 for camera flicker

OFF = 0.000
LOW = 33.33
MEDIUM = 66.66
HIGH = 100.0

MAX_DUTY_CYCLE = 65535

CLOSET_LIGHT_TIMEOUT = 30 # Units = Seconds

FAST_API_URL = '127.0.0.1:8000'

def set_brightness(light, value: float):
    """ Four light levels defined by PWM resolution 2^16 for ranges between 0 to 65535
    """
    dutyCycle = int((value/100.0)*MAX_DUTY_CYCLE)
    print(dutyCycle)
    light.duty_u16(dutyCycle)
    time.sleep(1/NON_FLICKER_FREQ)
    

def sync_remote_switch_to_app(self):
    """ Read from webserver running on Pi Pico 
    """
    pass sync_remote_switch_to_app

def sync_client(self, switchControllerId):
    """" GET from webserver running FastAPI on ZimaBoard using HouseAPI.py  
    """
    request = requests.get(FAST_API_URL)
    print(request)     #print(request.content)


def auto_ligth_shutdown(self, switchControllerId, timeout=CLOSET_LIGHT_TIMEOUT):
    pass


if __name__ == "__main__":
    print("Starting SwitchController.py using microPython on a Pi Pico")
    
    lights = PWM(Pin(2))    				# Pin = GP2 = PWM_A[1]
    lights.freq(NON_FLICKER_FREQ)
    set_brightness(lights, LOW)

    print("Attempt to connect to the Wifi")
    wifiObject = NetworkConfig()