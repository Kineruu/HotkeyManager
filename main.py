
# Imports
from pynput import keyboard as kb 
import webbrowser, threading, json
import customtkinter as ct

# Loading config
with open("config.json", "r") as f: 
    config = json.load(f)

HOTKEY = config["HOTKEY"]
DEFAULT_PREFIX = config["DEFAULT_PREFIX"]
SEARCH = config["SEARCH"]
SHORTCUTS = config["SHORTCUTS"]

history = []
history_number = 0

# Customtinker settings
window = ct.CTk() # Setting up the window
window.resizable(False, False) # So it can't be expanded.
window.overrideredirect(True) # Removes title bar

# Container frame
frame = ct.CTkFrame(window, corner_radius=5)
frame.pack(expand=True, fill="both", padx=4, pady=4)

# Dark mode
ct.set_appearance_mode("dark")
ct.set_default_color_theme("dark-blue") 

# Making the entry box, where user is able to write the commands
entry_input = ct.CTkEntry(frame, height=80, border_width=0)
entry_input.pack(side="left", fill="both", expand=True, padx=(6, 2), pady=6)

def hide(): window.withdraw() # Hides the window

# Didn't want to include this at first but for easier use I added it
close_button = ct.CTkButton(frame, text="x", width=20, height=20, command=hide, fg_color="transparent", hover_color="#333333")
close_button.pack(side="right", padx=(0, 6), pady=6)

# Putting it in the middle
window.update()
x = (window.winfo_screenwidth() // 2) - 110
y = (window.winfo_screenheight() // 2) - 20
window.geometry(f"220x40+{x}+{y}")

# Hiding it
window.withdraw()

def focus_window():
    window.deiconify() # Show window
    window.lift() # Show it above other windows
    window.attributes("-topmost", True) # Bring it to the front

    entry_input.focus_force()
    entry_input.select_range(0, "end") # Select all text

def run_command(text: str):
    if not text:
        return
    
    command, *rest = text.split(" ", 1)
    argument = rest[0] if rest else ""

    # Checks whether it's a search command first (for example yt cats)
    if command in SEARCH and argument:
        webbrowser.open(SEARCH[command] + argument)
        return

    # If it's a shortcut (gh -> github)
    if command in SHORTCUTS:
        webbrowser.open(SHORTCUTS[command])
        return

    if DEFAULT_PREFIX in SEARCH:
        webbrowser.open(SEARCH[DEFAULT_PREFIX] + text)

def on_enter(event=None):
    global history_number

    text = entry_input.get().strip() # Get text from the entry box
    if text:
        history.append(text)
        history_number = len(history)

    run_command(text) 
    entry_input.delete(0, "end") # Clears input
    window.withdraw() # Hiddens the window

def moving_history(step: int):
    global history_number
    if not history: return
    
    history_number = max(1, min(len(history), history_number + step))
    entry_input.delete(0, "end")
    entry_input.insert(0, history[-history_number])

# Converts config format to pynput one
def replace_hotkey(hotkey: str):
    return hotkey.lower().replace("ctrl", "<ctrl>").replace("shift", "<shift>").replace("alt", "<alt>")

def start_hotkey():
    # Global hotkey listener
    kb.GlobalHotKeys({ replace_hotkey(HOTKEY): focus_window }).run()

threading.Thread(target=start_hotkey, daemon=True).start() # Listening in the background

window.bind("<Escape>", lambda e: window.withdraw()) # Pressing escape hides the window
entry_input.bind("<Return>", on_enter) # Enter key runs the command in the entry box
entry_input.bind("<Up>", lambda e: moving_history(1))
entry_input.bind("<Down>", lambda e: moving_history(-1))

# Starts the GUI loop
window.mainloop()
