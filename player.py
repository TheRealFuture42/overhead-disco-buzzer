import random
import os
import pygame
from gpiozero import InputDevice, LED
import time

MUSIC_DIR = '/home/pi/Projects/MusicPlayer/music'

button = InputDevice(5)
led = LED(13)

# Pygame .init
pygame.mixer.init()

last_song = None

def play_random_song():
    global last_song
    print("Button was pressed")

    songs = [f for f in os.listdir(MUSIC_DIR) if f.endswith('.mp3')]

    if last_song:
        songs.remove(last_song)

    current_song = random.choice(songs)
    last_song = current_song
    print(f"Song: {current_song}")

    pygame.mixer.music.load(os.path.join(MUSIC_DIR, current_song))
    time.sleep(0.1)
    pygame.mixer.music.play()

    led.on()
    time.sleep(5)

    led.blink(on_time=0.5, off_time=0.5)

    song_skipped = False
    start_time = time.time()
    while pygame.mixer.music.get_busy():
        elapsed_time = time.time() - start_time

        if elapsed_time > 0.5 and button.value:
            pygame.mixer.music.stop()
            song_skipped = True
            break

        time.sleep(0.1)

    led.off()

    return song_skipped

while True:
    if button.value:
        song_skipped = play_random_song()
        if song_skipped:
            time.sleep(0.2)
            play_random_song()
        else:
            time.sleep(0.5)
