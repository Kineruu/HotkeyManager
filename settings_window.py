
from pynput import keyboard as kb

import customtkinter as ct
import json, os

with open("config.json", "r+") as f: 
    config = json.load(f)

HOTKEY = config["HOTKEY"]
DEFAULT_PREFIX = config["DEFAULT_PREFIX"]
SEARCH = config["SEARCH"]
SHORTCUTS = config["SHORTCUTS"]
FOLDERS = config["FILES"]
MAPPED_HOTKEYS = config["MAPPED_HOTKEYS"]

settings_window = ct.CTk()
settings_window.title("Settings")
settings_window.resizable(False, False)
#settings_window.overrideredirect(True)

settings_frame = ct.CTkFrame(settings_window, corner_radius=5)
settings_frame.pack(expand=True, fill="both", padx=4, pady=4)

for keys, value in config.items():
    json_label = ct.CTkLabel(settings_frame, text=keys)
    json_label.pack()

    if isinstance(value, dict):
        for sub_key, sub_value in value.items():
            sub_label = ct.CTkLabel(settings_frame, text=f"{sub_key}: {sub_value}")
            sub_label.pack()
    else:
        value_label = ct.CTkLabel(settings_frame, text=str(value))
        value_label.pack()

settings_window.mainloop()