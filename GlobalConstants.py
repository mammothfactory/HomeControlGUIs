#!/usr/bin/env python3
"""
__authors__    = ["Blaze Sanders"]
__contact__    = "blazes@mfc.us"
__copyright__  = "Copyright 2023"
__license__    = "GPLv3"
__status__     = "Development
__deprecated__ = False
__version__    = "0.0.1"
__doc__        = "CONSTANTS for both LiteHouse and Lustron home configurations"
"""
TODO = -1  

# Disable PyLint linting messages
# https://pypi.org/project/pylint/
# pylint: disable=invalid-name

ROOM_DEFINITION = 4
VALID_USA_CANADA_MEXICO_PHONE_NUMBER_LENGTH = 10

LITEHOUSE = 'LITEHOUSE'
LUSTRON = 'LUSTRON'

RUN_ON_NATIVE_OS = False
TUNNEL_TO_INTERNET = True

MAC_HOME_DIRECTORY   = '/Users/mars/MammothGithub/HomeControlGUIs'
LINUX_HOME_DIRECTORY = '/home/casaos/HomeControlGUIs'

LOCAL_HOST_PORT_FOR_GUI = 8181

MAMMOTH_BRIGHT_GRREN = '#03C04A'       #'background-color: #03C04A'

# LiteHouse Room Name Constants (a room can be defined by multiple rectangles)
# ?_X is the horizontal image pixel location of upper left corner of a rectangle in a room
# ?_Y is the vertical image pixel location of upper left corner of a room
# ?_X_WIDTH is the distance in image pixels between the far left and right of a rectangle in a room
# ?_Y_HEIGHT is the distance in image pixels between the top and bottom of a rectangle in a room
MASTER_BEDROOM = 'MASTER_BEDROOM'
MASTER_BEDROOM_SWITCH_PORT = 10
MASTER_BEDROOM_X = [1986]
MASTER_BEDROOM_Y = [97]
MASTER_BEDROOM_X_WIDTH = [806]
MASTER_BEDROOM_Y_HEIGHT = [815]
MAX_AREA_INDEX_MASTER_BEDROOM = 1
MASTER_BEDROOM_RECT_AREAS = [[MASTER_BEDROOM_X[0], MASTER_BEDROOM_Y[0], MASTER_BEDROOM_X_WIDTH[0], MASTER_BEDROOM_Y_HEIGHT[0]],]

MASTER_BATHROOM = 'MASTER_BATHROOM'
MASTER_BATHROOM_SWITCH_PORT = 11
MASTER_BATHROOM_X = [1520]        # X pixel location of upper left corner
MASTER_BATHROOM_Y = [361]
MASTER_BATHROOM_X_WIDTH = [432]
MASTER_BATHROOM_Y_HEIGHT = [553]
MAX_AREA_INDEX_MASTER_BATHROOM = 1
MASTER_BATHROOM_RECT_AREAS = [[MASTER_BATHROOM_X[0], MASTER_BATHROOM_Y[0], MASTER_BATHROOM_X_WIDTH[0], MASTER_BATHROOM_Y_HEIGHT[0]],]

KITCHEN = 'KITCHEN'
KITCHEN_SWITCH_PORT = 12
KITCHEN_X = [1099]        # X pixel location of upper left corner
KITCHEN_Y = [330]
KITCHEN_X_WIDTH = [390]
KITCHEN_Y_HEIGHT = [584]
MAX_AREA_INDEX_KITCHEN = 1
KITCHEN_RECT_AREAS = [[KITCHEN_X[0], KITCHEN_Y[0], KITCHEN_X_WIDTH[0], KITCHEN_Y_HEIGHT[0]],]

LIVINGROOM = 'LIVINGROOM'
LIVINGROOM_SWITCH_PORT = 13
LIVINGROOM_X = [284]        # X pixel location of upper left corner
LIVINGROOM_Y = [330]
LIVINGROOM_X_WIDTH = [815]
LIVINGROOM_Y_HEIGHT = [584]
MAX_AREA_INDEX_LIVINGROOM = 1
LIVINGROOM_RECT_AREAS = [[LIVINGROOM_X[0], LIVINGROOM_Y[0], LIVINGROOM_X_WIDTH[0], LIVINGROOM_Y_HEIGHT[0]],]

HALLWAY = 'HALLWAY'
HALLWAY_SWITCH_PORT = 14
HALLWAY_X = [TODO]        # X pixel location of upper left corner
HALLWAY_Y = [TODO]
HALLWAY_X_WIDTH = [TODO]
HALLWAY_Y_HEIGHT = [TODO]
MAX_AREA_INDEX_HALLWAY = 1
HALLWAY_RECT_AREAS = [[HALLWAY_X[0], HALLWAY_Y[0], HALLWAY_X_WIDTH[0], HALLWAY_Y_HEIGHT[0]],]


# Lustron Room Name Constants
BEDROOM_2 = 'BEDROOM_2'
BEDROOM_2_X = [TODO, TODO]                    # X pixel location of upper left corner
BEDROOM_2_Y = [TODO, TODO]
BEDROOM_2_X_WIDTH = [TODO, TODO]
BEDROOM_2_Y_HEIGHT = [TODO, TODO]
MAX_AREA_INDEX_BEDROOM_2 = 2
BEDROOM_2_RECT_AREAS = [[BEDROOM_2_X[0], BEDROOM_2_Y[0], BEDROOM_2_X_WIDTH[0], BEDROOM_2_Y_HEIGHT[0]], \
                        [TODO, TODO, TODO, TODO]]

BEDROOM_3 = 'BEDROOM_3'
BEDROOM_3_X = [TODO]                    # X pixel location of upper left corner
BEDROOM_3_Y = [TODO]
BEDROOM_3_X_WIDTH = [TODO]
BEDROOM_3_Y_HEIGHT = [TODO]
MAX_AREA_INDEX_BEDROOM_3 = 1
BEDROOM_3_RECT_AREAS = [[BEDROOM_3_X[0], BEDROOM_3_Y[0], BEDROOM_3_X_WIDTH[0], BEDROOM_3_Y_HEIGHT[0]],]

BATHROOM_2 = 'BATHROOM_2'
BATHROOM_2_X = [TODO]                   # X pixel location of upper left corner
BATHROOM_2_Y = [TODO]
BATHROOM_2_X_WIDTH = [TODO]
BATHROOM_2_Y_HEIGHT = [TODO]
MAX_AREA_INDEX_BATHROOM_2 = 1
BATHROOM_2_RECT_AREAS = [[BATHROOM_2_X[0], BATHROOM_2_Y[0], BATHROOM_2_X_WIDTH[0], BATHROOM_2_Y_HEIGHT[0]],]

# Interactive image filenames for square blur (aka V1) yellow light overlay
LITE_HOUSE_SOURCE = 'static/images/LiteHouseV1_00000.png'
LITE_HOUSE_SOURCE00000001 = 'static/images/LiteHouseV1_00001.png'
LITE_HOUSE_SOURCE00000010 = 'static/images/LiteHouseV1_00010.png'
LITE_HOUSE_SOURCE00000011 = 'static/images/LiteHouseV1_00011.png'
LITE_HOUSE_SOURCE00000100 = 'static/images/LiteHouseV1_00100.png'
LITE_HOUSE_SOURCE00000101 = 'static/images/LiteHouseV1_00101.png'
LITE_HOUSE_SOURCE00000110 = 'static/images/LiteHouseV1_00110.png'
LITE_HOUSE_SOURCE00000111 = 'static/images/LiteHouseV1_00111.png'
LITE_HOUSE_SOURCE00001000 = 'static/images/LiteHouseV1_01000.png'
LITE_HOUSE_SOURCE00001001 = 'static/images/LiteHouseV1_01001.png'
LITE_HOUSE_SOURCE00001010 = 'static/images/LiteHouseV1_01010.png'
LITE_HOUSE_SOURCE00001011 = 'static/images/LiteHouseV1_01011.png'
LITE_HOUSE_SOURCE00001100 = 'static/images/LiteHouseV1_01100.png'
LITE_HOUSE_SOURCE00001101 = 'static/images/LiteHouseV1_01101.png'
LITE_HOUSE_SOURCE00001110 = 'static/images/LiteHouseV1_01110.png'
LITE_HOUSE_SOURCE00001111 = 'static/images/LiteHouseV1_01111.png'
LITE_HOUSE_SOURCE00010000 = 'static/images/LiteHouseV1_10000.png'
LITE_HOUSE_SOURCE00010001 = 'static/images/LiteHouseV1_10001.png'
LITE_HOUSE_SOURCE00010010 = 'static/images/LiteHouseV1_10010.png'
LITE_HOUSE_SOURCE00010011 = 'static/images/LiteHouseV1_10011.png'
LITE_HOUSE_SOURCE00010100 = 'static/images/LiteHouseV1_10100.png'
LITE_HOUSE_SOURCE00010101 = 'static/images/LiteHouseV1_10101.png'
LITE_HOUSE_SOURCE00010110 = 'static/images/LiteHouseV1_10110.png'
LITE_HOUSE_SOURCE00010111 = 'static/images/LiteHouseV1_10111.png'
LITE_HOUSE_SOURCE00011000 = 'static/images/LiteHouseV1_11000.png'
LITE_HOUSE_SOURCE00011001 = 'static/images/LiteHouseV1_11001.png'
LITE_HOUSE_SOURCE00011010 = 'static/images/LiteHouseV1_11010.png'
LITE_HOUSE_SOURCE00011011 = 'static/images/LiteHouseV1_11011.png'
LITE_HOUSE_SOURCE00011100 = 'static/images/LiteHouseV1_11100.png'
LITE_HOUSE_SOURCE00011101 = 'static/images/LiteHouseV1_11101.png'
LITE_HOUSE_SOURCE00011110 = 'static/images/LiteHouseV1_11110.png'
LITE_HOUSE_SOURCE00011111 = 'static/images/LiteHouseV1_11111.png'


LUSTRON_SOURCE = 'static/images/LustronV1_00000000.png'


STATIC_DEFAULT_NETWORK = '''
                graph LR;
                    A[UniFi PoE Switch] --> B[ROOM: Master Bedroom];
                    A[UniFi PoE Switch] --> F[ZimaBoard Server];
                    F[CPU: ZimaBoard Server] --> E[DISPLAY: Main Central Control];
                    B[ROOM: Master Bedroom] --> C[LIGHT: Master Bedroom]; 
                    B[ROOM: Master Bedroom] --> D[DISPLAY: Master Bedroom];
                    A[UniFi PoE Switch] --> G[LIGHT-Kitchen];
                    
                    style A color:#000000, fill:#03C04A, stroke:#000000;
                    style B color:#000000, fill:#03COFF, stroke:#000000;
                    style C color:#000000, fill:#FFC04A, stroke:#000000;
                    style D color:#FFFFFF, fill:#1F1F1F, stroke:#000000;
                    style E color:#FFFFFF, fill:#1F1F1F, stroke:#000000;
                    style F color:#000000, fill:#B8191D, stroke:#000000;
                    style G color:#000000, fill:#FFC04A, stroke:#000000;
                '''


# Error Codes
# https://pagekite.net/support/service_api_reference/#error_codes
BAD_VALUE = "Bad value for"
BAD_KEY = "Invalid key"
BAD_USERS = "Invalid e-mails or kite names"
BAD_GROUP = "Invalid group ID"
DNS_ERROR = "DNS Error"
DOMAIN = "Domain unavailable"
domaintaken = "Domain is already in use"
email = "Invalid e-mail address"
emailtaken = "E-mail is already in use"
error = "Internal Error"
kite_gone = "No such kite, was it already deleted?"
no_account = "No such account exists"
no_groups = "You cannot create any more groups"
no_members = "That would exceed your membership limit!"
no_root_ns = "Could not find root nameserver"
no_service = "Not a service domain"
not_cname = "CNAME record not found"
not_in_group = "You are not in a group"
pass_mismatch = "Passwords do not match"
pass_short = "Passwords is too short"
pleaselogin = "Please log in"
subdomain = "Invalid kite name"
terms = "Please accept the terms and conditions"
unauthorized = "Access Denied"
unchanged = "Nothing has changed"
undo_key = "Invalid Undo Key"
unregistered = "Not a registered kite"