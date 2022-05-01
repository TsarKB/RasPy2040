## SPDX-FileCopyrightText: 2022 Tsar Keyboards
# SPDX-License-Identifier: GNU GPL3.0
# RasPy 2040

import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

KC = Keycode
CC = ConsumerControlCode

DT_END    = 10 # The amount of time (in hundredths of a second) in which the user can re-hit the key to trigger the secondary function
HOLD_TIME = 10 # The amount of time (in hundredths of a second) a user must hold a key to trigger a hold action.

MED  = 1 # MED key - see https://circuitpython.readthedocs.io/projects/hid/en/latest/ for keycodes
KEY  = 2 # Standard keyboard key - see https://circuitpython.readthedocs.io/projects/hid/en/latest/ for keycodes
LSW  = 3 # Switch Layers
MAC  = 4 # Will output a Macro
STR  = 5 # Will output a full string
RES  = 6 # Resets the pi, will put you in bootloader or safe mode.
FUNC = 7 # Runs a user-defined function. For advanced use only.
DT   = 8 # Used as a third argument to allow a user to double-tap a key to get a secondary action, ie (KEY, (KC.ESCAPE), DT, KEY, (KC.ONE))
HOLD = 9 # Used as a third argument to allow a user to hold a key to get a secondary action, ie (KEY, (KC.ESCAPE), HOLD, KEY, (KC.ONE))

#Define the rows and columns that the wires or traces that are connected to your board.
COLS  = [0,28,27,26]
ROWS  = [2,3,4,5,6]

# Add in your macros and strings as variables here. This isn't strictly necessary, but makes your keymap look much more readable.
# For strings, \n = line break, \t = tab
# Macros are sent as tuples. Macros have a maximum length of six keys.

helloWorld   = "Hello \n\t World!" # Outputs "Hello World". The \n represents a carriage return, and the \t is a tab.
macroExample = (KC.LEFT_CONTROL, KC.LEFT_ALT, KC.DELETE) # Macro for Alt + Ctrl + Del. 

# Just lay this out physically like your keyboard is laid out.  Ie, the top left key should be keymap[0][0][0] or Backspace in this example
keymap = [
    [
        [ (KEY, (KC.BACKSPACE)), (KEY, (KC.KEYPAD_FORWARD_SLASH)), (KEY, (KC.KEYPAD_ASTERISK)), (KEY, (KC.MINUS)) ],
        [ (KEY, (KC.KEYPAD_SEVEN)), (KEY, (KC.KEYPAD_EIGHT)), (KEY, (KC.KEYPAD_NINE)), None ],
        [ (KEY, (KC.KEYPAD_FOUR)), (KEY, (KC.KEYPAD_FIVE)), (KEY, (KC.KEYPAD_SIX)), (KEY, (KC.KEYPAD_PLUS)) ],
        [ (KEY, (KC.KEYPAD_ONE)), (KEY, (KC.KEYPAD_TWO)), (KEY, (KC.KEYPAD_THREE)), None ],
        [ (STR, '00', HOLD, LSW, 1), (KEY, (KC.KEYPAD_ZERO)), (KEY, (KC.KEYPAD_PERIOD)), (KEY, (KC.KEYPAD_ENTER)) ],
    ],
    [
        [ (KEY, (KC.KEYPAD_NUMLOCK)), None, None, (RES, 'boot') ],
        [ None, None, None, None ],
        [ None, None, None, None ],
        [ None, None, None, None ],
        [ (LSW, 1), (STR, helloWorld), None, (RES, 'safe') ],
    ],
]

# Define your rotary encoders here.  Out A and Out B are are the left/right pins on your encoder. Switch, if you have it, is the pin called SW that is 
# actiavted when you press the encoder down. Not all encoders have this switch, so it can be set to None if you don't have it or don't wish to use it.
# The keymap is formatted in layers and MUST have the same amount of layers as your keymap or you could get errors. The mapping is as follows:
# [ (LEFT ACTION), (CLICK ACTION), (RIGHT ACTION) ]
# Actual Example:
# [ (MED, (CC.VOLUME_DECREMENT), (MED, (CC.MUTE)), (MED, (CC.VOLUME_INCREMENT)) ] --Left = volume down, click = mute, right = volume up.

encoder_map = []

toggle_map = []