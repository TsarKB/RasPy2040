## SPDX-FileCopyrightText: 2021 Nick Bell Aviator Ortho 40%
# SPDX-License-Identifier: MIT
# RaspberryPi Pico RP2040 Keyboard Functions

import board
import rotaryio
import time
from digitalio import DigitalInOut, Direction, Pull

# list of pins to use (skipping GP15 on Pico because it's funky)
pins = [
    board.GP0,
    board.GP1,
    board.GP2,
    board.GP3,
    board.GP4,
    board.GP5,
    board.GP6,
    board.GP7,
    board.GP8,
    board.GP9,
    board.GP10,
    board.GP11,
    board.GP12,
    board.GP13,
    board.GP14,
    board.GP15,  #Don't use this pin due to weirdness
    board.GP16,
    board.GP17,
    board.GP18,
    board.GP19,
    board.GP20,
    board.GP21,
    board.GP22,
    board.GP23,
    board.GP24,
    board.GP25,
    board.GP26,
    board.GP27,
    board.GP28,
]

# Take in the formatted key map that the user has set and add in the necessary hooks to control them.
# Layers should come in the following format:
# [
#     [ # Layer 0
#         [(Type, Value), (Type, Value)], # Row 1
#         [(Type, Value), (Type, Value)], # Row 2
#         [(Type, Value), (Type, Value)], # Row 3
#         [(Type, Value), (Type, Value)], # Row 4
#     ],
#     [ # Layer 1
#         [(Type, Value), (Type, Value)], # Row 1
#         [(Type, Value), (Type, Value)], # Row 2
#         [(Type, Value), (Type, Value)], # Row 3
#         [(Type, Value), (Type, Value)], # Row 4
#     ],
# ]

def initializeLayerMap(layers):
    completeMap = []
    for layer in range(len(layers)):
        rows     = layers[layer]
        newLayer = []
        completeMap.append(newLayer)
        for row in range(len(rows)):
            keys = rows[row]
            completeMap[layer].append([])
            for key in range(len(keys)):
                thisKey = keys[key]
                newRow  = completeMap[layer][row]
                
                # If this key has been intentionally left blank, just set it as None and continue to another key.
                if thisKey == None :
                    newRow.append(None)
                    continue 
                # Initialize the alternate values as None. These are only set on special keys.
                altFunc  = None
                altType  = None
                altValue = None

                # Check if this is a special key. If so, add in the alternate
                if (len(thisKey) > 2) :
                    altFunc  = thisKey[2]
                    altType  = thisKey[3]
                    altValue = thisKey[4]
                
                newRow.append({
                     "status"   : 0,
                     "dt"       : 0, # Delta time - used to determine how long the user has been holding down the key.
                     "tap"      : False, # Whether the first tap has occurred on a double tap action.
                     "type"     : thisKey[0], #This gets the TYPE of the key in the layout.
                     "value"    : thisKey[1] , # This gets the actual value in the keymap.
                     "altFunc"  : altFunc, # If there is an alternate function, determine what it is.
                     "altType"  : altType, # See type above, for the alternate keystroke to register.
                     "altValue" : altValue,
                     "debounce" : False, # When holding or double-tapping, set this to true to stop multiple accidental inputs
                })            

    return completeMap

#This just enumerates all the pins on the pi pico that can be used.
def mapSwitches(ROWS,COLS) :
    switches = [0, 1, 2, 3, 4, 5, 6,
                7, 8, 9, 10, 11, 12, 13,
                14, 15, 16, 17, 18, 19, 20, 21, 22, 23,24,25, 26, 27, 28]

    # Make each row an input.
    for j in ROWS:
        switches[j]           = DigitalInOut(pins[j])
        switches[j].direction = Direction.INPUT
        switches[j].pull      = Pull.DOWN
    #Make each column an output.  Looping through each column, then each row will tell us which key is being pressed when.
    for k in COLS:
        switches[k] = DigitalInOut(pins[k])
        switches[k].direction = Direction.OUTPUT
    
    return switches

# Takes the encoder mapping as set up by the user and adds in the encoder object and button object to be checked.
def initializeRotaryEncoders(encoder_map) :
    # Initialize the encoder and set it on the encoder map object.
    encoder_map['encoder']  = rotaryio.IncrementalEncoder(pins[encoder_map['pins']['out_a']], pins[encoder_map['pins']['out_b']])
    encoder_map['position'] = 0

    # Initialized the button object so we can set it.
    newButton             = DigitalInOut(pins[encoder_map['pins']['switch']])
    newButton.direction   = Direction.INPUT
    newButton.pull        = Pull.UP # Encoder must use pull UP. Down will cause all kinds of weird issues.
    encoder_map['button'] = newButton
    

# Checks the rotary encoder(s) each cycle and returns the appropriately mapped key.
def checkEncoder(encoder) :
    # Determine if the encoder has been rotated
    current_position = encoder['encoder'].position
    position_change  = current_position - encoder['position']
    encoderIndex     = None # This is the value we'll send to the main loop if any change has occurred.
    if position_change > 0 :
        print('UP')
        encoderIndex = 2
    elif position_change < 0 :
        print('DOWN') 
        encoderIndex = 0
    
    encoder['position'] = current_position # Set the position to our new position so we can compare again later. 

    # Check if the encoder's button has been pressed.
    if not encoder['button'].value and not encoder['clicked']:
        print('CLICK')
        encoder['clicked'] = True #Set the encoder back to false once the key has been sent.
        encoderIndex = 1
    
    if encoder['button'].value and encoder['clicked'] :
        encoder['clicked'] = False

    return encoderIndex

# Using the toggle_map in the keymap file, initialize any toggle switches on the board.
def initializeToggleSwitches(switch) :
    switch['status'] = False

    newSwitch           = DigitalInOut(pins[switch['pin']])
    newSwitch.direction = Direction.INPUT
    newSwitch.pull      = Pull.UP # Encoder must use pull UP. Down will cause all kinds of weird issues.
    switch['switch']    = newSwitch

# On each cycle, check to see if the switch has changes status.  If so, return the action to be performed.
def checkToggle(switch) :
    if switch['switch'].value and switch['status'] != switch['switch'].value :
        switch['status'] = switch['switch'].value
        print('ON')
        return switch['action']
    elif not switch['switch'].value and switch['status'] != switch['switch'].value :
        switch['status'] = switch['switch'].value
        print('OFF')
        return switch['action']

def spongeBob() :
    print('SPONGEBOB SQUAREPANTS!!')