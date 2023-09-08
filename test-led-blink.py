from gpiozero import LED
import time

led = LED(13)

while True:
    led.blink(on_time=0.5, off_time=0.5)
    time.sleep(5)
    led.off()
    time.sleep(5)
