""" 
Main.py

    An example using bitmap to draw sprites on the display.

    Spritesheet from CircuitPython_Flying_Toasters
    https://learn.adafruit.com/circuitpython-sprite-animation-pendant-mario-clouds-flying-toasters

"""

import random
from machine import Pin, SPI
import GC9A01 as gc9a01
import mfcLogo, fanLogo
import t1, t2, t3, t4, t5

MFC_ICON = [mfcLogo]
FAN_ICON = [fanLogo]   # List of time slices for animated fan logo
#LOUVRE_ICON = [louvreLogo]
#LINES = []

class BitMapItem():
    '''
    BitMapItem class to keep track of a sprites locaton
    '''
    def __init__(self, sprites, x, y):
        self.sprites = sprites
        self.x = x
        self.y = y



def main():
    """
    Initialize the display and draw flying toasters and toast
    """
    spi = SPI(0, baudrate=60000000, sck=Pin(18), mosi=Pin(19))   # MOSI = SPI? TX
    tft = gc9a01.GC9A01(
        spi,
        dc=Pin(13, Pin.OUT),  # Data / Command Pin
        cs=Pin(21, Pin.OUT),  # Chip Select Pin n
        reset=Pin(16, Pin.OUT),
        backlight=Pin(14, Pin.OUT),
        rotation=0)

    tft.fill(gc9a01.BLACK)
    
    # Create toast spites in specific positions
    sprites = [
        BitMapItem(FAN_ICON, 40, 60),
        BitMapItem(MFC_ICON, 180, 180),
    ]

    for iconNum in sprites:
        bitmap = iconNum.sprites
        tft.bitmap(bitmap, iconNum.sprites.x, iconNum.sprites.y)
    """
    # move and draw sprites
    while True:
        for man in sprites:
            bitmap = man.sprites[man.step]
            tft.fill_rect(
                man.x+bitmap.WIDTH-man.speed,
                man.y,
                man.speed,
                bitmap.HEIGHT,
                gc9a01.BLACK)

            man.move()

            if man.x > 0:
                tft.bitmap(bitmap, man.x, man.y)
            else:
                tft.fill_rect(
                    0,
                    man.y,
                    bitmap.WIDTH,
                    bitmap.HEIGHT,
                    gc9a01.BLACK)

    """
main()


