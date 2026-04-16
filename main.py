
from pynput import keyboard as kb

import customtkinter as ct
import webbrowser
import threading
import json

with open("config.json", "r") as f:
    config = json.load(f)

shortcuts = config["SHORTCUTS"]

window = ct.CTk()
#window.geometry("220x40")
window.resizable(False, False)
window.overrideredirect(True)

frame = ct.CTkFrame(window, corner_radius=5)
frame.pack(expand=True, fill="both", padx=4, pady=4)

ct.set_appearance_mode("dark")
ct.set_default_color_theme("dark-blue")

entry_input = ct.CTkEntry(frame, height=80, border_width=0)
entry_input.pack(side="left", fill="both", expand=True, padx=(6, 2), pady=6)

def close_window(): window.withdraw()

close_button = ct.CTkButton(frame, text="x", width=20, height=20, command=close_window, fg_color="transparent", hover_color="#333333")
close_button.pack(side="right", padx=(0, 6), pady=6)

window.update()
x = (window.winfo_screenwidth() // 2) - 110
y = (window.winfo_screenheight() // 2) - 20
window.geometry(f"220x40+{x}+{y}")

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
    part = text.split(" ", 1)
    command = part[0]

    if command in config["SEARCH"] and len(part) > 1:
        search = part[1]
        base_url = config["SEARCH"][command]
        webbrowser.open(base_url + search)
        return

    if command in shortcuts:
        webbrowser.open(shortcuts[command])
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
