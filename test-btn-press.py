from gpiozero import InputDevice
import time

button = InputDevice(5)

while True:
    if button.value:
        print("Button gedrückt!")
        time.sleep(0.5)
