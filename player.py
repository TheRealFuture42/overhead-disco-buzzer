import random
import os
import pygame
from gpiozero import InputDevice, LED
import time

MUSIC_DIR = '/home/pi/Projects/MusicPlayer/music'

# GPIOs
button = InputDevice(5)
led = LED(13)

# Pygame init
pygame.mixer.init()

last_song = None

def play_random_song():
    global last_song
    print("Button was pressed")

    # Get all mp3 files in music directory
    songs = [f for f in os.listdir(MUSIC_DIR) if f.endswith('.mp3')]

    if not songs:
        print("No songs found.")
        return

    # Remove last song from list to avoid playing it again
    if last_song and last_song in songs:
        songs.remove(last_song)

    # Choose a random song
    current_song = random.choice(songs)
    # Save last song
    last_song = current_song
    print(f"Song: {current_song}")

    # Load & Play song
    pygame.mixer.music.load(os.path.join(MUSIC_DIR, current_song))
    pygame.mixer.music.play()

    led.blink(on_time=0.5, off_time=0.5) # Blink LED while song is playing
    time.sleep(5) # Wait x times in seconds before checking if button is pressed
    led.blink(on_time=0.2, off_time=0.2) # Blink LED faster to indicate that button can be pressed to skip song

    # Wait for song to finish
    song_skipped = False
    start_time = time.time()

    # Button can be pressed to skip song after 0.5 seconds
    while pygame.mixer.music.get_busy(): 
        elapsed_time = time.time() - start_time 

        if elapsed_time > 0.5 and button.value: 
            pygame.mixer.music.stop() 
            song_skipped = True
            break 

        time.sleep(0.2)

    return song_skipped

while True:
    led.on() # Turn on LED

    if button.value:
        song_skipped = play_random_song() # Play song
        if song_skipped: # If song was skipped, wait a bit before playing another song
            time.sleep(0.2)
            play_random_song()
        else:
            time.sleep(0.5) # Wait a bit before playing another song
