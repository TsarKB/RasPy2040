# RasPy2040
### Keyboard firmware created with circuitPython for Raspberry Pi 2040 devices.
RasPy 2040 is a new keybaord firmware based on [CircuitPython](https://circuitpython.org/) and [Adafruit's USB HID Library](https://docs.circuitpython.org/en/latest/shared-bindings/usb_hid/index.html). RasPy 2040 is designed to allow users to create their own keyboards using the RP2040 chip by the Raspberry Pi Foundation, and currently supports any board using this chip. The current version is being used on a Raspberry Pi Pico, but could be used on anything containing the RP2040 chip, provided the GPIO pins are available.

####The following features are currently supported:
* Layers - Users can add as many layers as they wish, with the only constraint being the storage space of their device.
* Macros - Users can define macros and place them on layers to be performed when a key or combination of keys is pressed.
* String Output - Similar to macros, a user can output full strings and blocks of text.
* Consumer control Keys - Configure your keyboard to change volume, play/pause music, and many other functions using consumer control codes.
* Rotary Encoders - Can also be used in conjunction with layers to allow for multiple actions for a single encoder.
* Toggle Switches
* Double-Tap Actions - Users can set a double-tap threshold for certain keys to allow more than one function based on how fast the key was hit in succession.
* Hold Actions - Users can add a secondary function to a key that is held down for a length of time.

####The following features are not supported but are on the roadmap:
* I2C communication to allow for creation of split keyboards, or keyboards that use more keys than is supported by the grid layout.
*   I2C displays
* Visual Interface to allow for users who don't want to code to alter their keymap/create new keyboard layouts.
* RGB!
