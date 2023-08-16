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
        print('Wifi connected!')
