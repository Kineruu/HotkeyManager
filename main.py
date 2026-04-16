
from pynput import keyboard as kb

import customtkinter as ct
import webbrowser
import threading
import json

with open("config.json", "r") as f:
    config = json.load(f)

shortcuts = config["SHORTCUTS"]

window = ct.CTk()
window.geometry("90x30")
window.resizable(False, False)

frame = ct.CTkFrame(master=window)
frame.pack()

ct.set_appearance_mode("dark")
ct.set_default_color_theme("dark-blue")

entry_input = ct.CTkEntry(frame, width=80, height=25)
entry_input.pack(side="left")

window.withdraw()

HOTKEY = config["HOTKEY"]

def show_window():
    window.deiconify()
    window.update_idletasks()

    window.attributes("-topmost", True)
    window.lift()

    window.after(150, lambda: focus_entry_box())
    window.after(100, lambda: window.attributes("-topmost", False))

    entry_input.delete(0, "end")

def focus_entry_box():
    entry_input.focus_force()
    entry_input.icursor("end")
    entry_input.select_range(0, "end")

def run_command(text):
    if text in shortcuts:
        webbrowser.open(shortcuts[text])
        return
    
    if text.startswith("g "):
        search = text[2:]
        webbrowser.open(f"https://www.google.com/search?q={search}")
        return

    if text.startswith("yt "):
        search = text[3:]
        webbrowser.open(f"https://www.youtube.com/results?search_query={search}")
        return

def on_enter(event=None):
    text = entry_input.get().strip()
    run_command(text)
    entry_input.delete(0, "end")
    window.withdraw()

window.bind("<Escape>", lambda e: window.withdraw())
entry_input.bind("<Return>", on_enter)

def replace_hotkey(hotkey: str):
    hotkey = hotkey.lower()
    return hotkey.replace("ctrl", "<ctrl>").replace("shift", "<shift>").replace("alt", "<alt>")

def start_hotkey():
    formatted_hotkey = replace_hotkey(HOTKEY)
    hotkey = kb.GlobalHotKeys({
        formatted_hotkey: show_window
    })
    hotkey.run()

threading.Thread(target=start_hotkey, daemon=True).start()
window.mainloop()
