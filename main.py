import keyboard
import time

"""
TODO:
-> Make it check for each keyboard letter?
-> Code a small window where I can put shortcuts in
gh -> github, yt -> youtube, yt something -> searches for something in youtube etc.
-> Maybe open up a cmd window who knows
"""

keys = input("KEYBIND: ")
if keys == "": keys = "ctrl+shift+c" # Default hotkey for now

def keyboard_listener():
    print("HOTKEY DETECTED")

keyboard.add_hotkey(keys, keyboard_listener)
print("Listening for keys, press ESC to quit.")
keyboard.wait("esc")