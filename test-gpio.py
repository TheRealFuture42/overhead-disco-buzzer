from gpiozero import InputDevice, LED
import time

button = InputDevice(5)
led = LED(13)

try:
    while True:
        print("Button Status (GPIO13):", button.value)
        print("LED Status (GPIO5):", led.value)

        time.sleep(1)

except KeyboardInterrupt:
    print("\nBeende Überwachung...")
