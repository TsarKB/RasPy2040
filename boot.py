import storage
import board
import microcontroller
from digitalio import DigitalInOut, Direction, Pull

# Determine if the numlock key is being held down.  If so, reboot into safe mode.
safePinOut = DigitalInOut(board.GP0)
safePinOut.direction = Direction.OUTPUT
safePinOut.value = True

safePinIn = DigitalInOut(board.GP1)
safePinIn.direction = Direction.INPUT

if safePinIn.value == True :
    print('Rebooted with Numlock held down.')
    microcontroller.on_next_reset(microcontroller.RunMode.SAFE_MODE)
    microcontroller.reset()

# safePinOut.value = False
storage.disable_usb_drive() # Ensure this doesn't show up as a USB drive.
usb_cdc.disable()              # Turn off REPL.
