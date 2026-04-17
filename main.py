
# Import section
from pynput import keyboard as kb 
import customtkinter as ct
import webbrowser
import threading
import json

# Loading the config.json file.
with open("config.json", "r") as f: config = json.load(f)
shortcuts = config["SHORTCUTS"]

# Customtinker settings
window = ct.CTk() # Setting up the window
window.resizable(False, False) # So it can't be expanded.
window.overrideredirect(True) # It removes windows manager (Removes title bar)

frame = ct.CTkFrame(window, corner_radius=5) # Makes a container inside my window
# Corner_radius = 5 so it's not that sharp
frame.pack(expand=True, fill="both", padx=4, pady=4) # Placing it

# Setting dark mode
ct.set_appearance_mode("dark")
ct.set_default_color_theme("dark-blue") 

# Making the entry box, where user is able to write the commands
entry_input = ct.CTkEntry(frame, height=80, border_width=0)
entry_input.pack(side="left", fill="both", expand=True, padx=(6, 2), pady=6)

def close_window(): window.withdraw() # Literally makes the window hidden

# Didn't want to include this at first but for easier use I added it
close_button = ct.CTkButton(frame, text="x", width=20, height=20, command=close_window, fg_color="transparent", hover_color="#333333")
close_button.pack(side="right", padx=(0, 6), pady=6)

# Putting it in the middle
window.update()
x = (window.winfo_screenwidth() // 2) - 110
y = (window.winfo_screenheight() // 2) - 20
window.geometry(f"220x40+{x}+{y}")

# Hiding it
window.withdraw()

# Basically what keys you have to press to show the window
HOTKEY = config["HOTKEY"]
DEFAULT_PREFIX = config["DEFAULT_PREFIX"]

def show_window():
    window.deiconify() # Show window
    window.update_idletasks() # Refresh it

    window.attributes("-topmost", True) # Bring it to the front
    window.lift() # Show it above other windows

    window.after(150, lambda: focus_entry_box()) # To avoid focus bugs, it is delayed
    window.after(100, lambda: window.attributes("-topmost", False)) 

    # Clears the previous text
    entry_input.delete(0, "end")

# Focus and select text inside entry
def focus_entry_box():
    entry_input.focus_force()

    entry_input.icursor("end") # Move cursor to the end
    entry_input.select_range(0, "end") # Select all text

def run_command(text):
    part = text.split(" ", 1)
    command = part[0]

    # Checks whether it's a search command first (for example yt cats)
    if command in config["SEARCH"] and len(part) > 1:
        search = part[1]
        base_url = config["SEARCH"][command]
        webbrowser.open(base_url + search)
        return

    # If it's a shortcut (gh -> github)
    if command in shortcuts:
        webbrowser.open(shortcuts[command])
        return
    
    if not text:
        return

    if DEFAULT_PREFIX in config["SEARCH"]: # Checks whether the default prefix is in config
        base_url = config["SEARCH"][DEFAULT_PREFIX]
        webbrowser.open(base_url + text)
        return 

def on_enter(event=None):
    text = entry_input.get().strip() # Get text from the entry box
    run_command(text) 
    entry_input.delete(0, "end") # Clears input
    window.withdraw() # Hiddens the window

window.bind("<Escape>", lambda e: window.withdraw()) # Pressing escape hides the window
entry_input.bind("<Return>", on_enter) # Enter key runs the command in the entry box

# Converts config format to pynput one
def replace_hotkey(hotkey: str):
    hotkey = hotkey.lower()
    return hotkey.replace("ctrl", "<ctrl>").replace("shift", "<shift>").replace("alt", "<alt>")

def start_hotkey():
    formatted_hotkey = replace_hotkey(HOTKEY)

    hotkey = kb.GlobalHotKeys({ # Global hotkey listener
        formatted_hotkey: show_window
    })
    # Starts it
    hotkey.run()

threading.Thread(target=start_hotkey, daemon=True).start() # Listening in the background
# Starts the GUI loop
window.mainloop()
