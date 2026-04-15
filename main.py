import customtkinter as ct
import keyboard
import threading
import webbrowser
import time
"""
TODO:
-> Make it check for each keyboard letter?
-> Code a small window where I can put shortcuts in
gh -> github, yt -> youtube, yt something -> searches for something in youtube etc.
-> Maybe open up a cmd window who knows
"""

window = ct.CTk()
window.geometry("100x50")
window.resizable(False, False)
frame = ct.CTkFrame(master=window)

entry_input = ct.CTkEntry(window, width=95, height=45)
entry_input.pack()

window.withdraw()

#keys = input("KEYBIND: ")
#if keys == "": keys = "ctrl+shift+c" # Default hotkey for now
keys = "ctrl+shift+c"

def show_window():
    window.deiconify()
    window.lift()
    window.focus_force()
    entry_input.focus()

def keyboard_listener(event=None):
    text = entry_input.get()
    print(f"HOTKEY DETECTED {text}")

    if text == "gh":
        webbrowser.open("https://github.com")
        window.withdraw()
    else:
        window.withdraw()
    
entry_input.bind("<Return>", keyboard_listener)

def start_listening():
    keyboard.add_hotkey(keys, show_window)
    keyboard.wait()

threading.Thread(target=start_listening, daemon=True).start()

window.mainloop()