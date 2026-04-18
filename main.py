
# Imports
from pynput import keyboard as kb 
import webbrowser, threading, json, win32gui, win32con, win32api, win32process, subprocess, time
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
window.title("Hotkey Manager GUI")
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

def focus_window_logic():
    # 1. Reveals window
    window.deiconify()
    
    # Grabbing the window's id that Windows assigned to my CTk
    my_hwnd = window.winfo_id() 
    # Asks windows what window is the user looking at right now
    fore_hwnd = win32gui.GetForegroundWindow()
    # Gets the thread ID the python script is running in
    thread_it = win32api.GetCurrentThreadId()
    fore_thread_id, _ = win32process.GetWindowThreadProcessId(fore_hwnd)
    
    # 3. Attach Thread Input
    if thread_it != fore_thread_id:
        try:
            # Links the script
            win32process.AttachThreadInput(fore_thread_id, thread_it, True)
            # Windows allows me to put the window in front
            win32gui.SetForegroundWindow(my_hwnd)
            win32gui.SetFocus(my_hwnd)
            # Unlinks the script
            win32process.AttachThreadInput(fore_thread_id, thread_it, False)
        except:
            pass
    
    # 4. Force Topmost briefly
    window.attributes("-topmost", True)
    
    # 5. Force Keyboard Focus
    entry_input.focus_force()
    entry_input.select_range(0, "end")
    
    # 6. Release Topmost so it doesn't stay stuck
    window.after(200, lambda: window.attributes("-topmost", False))

def focus_window():
    window.after(0, focus_window_logic)

def focus_window_by_pid(pid):
    def callback(hwnd, _):
        # Gets the thread ID
        _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
        if found_pid == pid and win32gui.IsWindowVisible(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
            return False 
        return True
    win32gui.EnumWindows(callback, None)

def run_command(text: str):
    if not text: return
    command, *rest = text.split(" ", 1)
    argument = rest[0] if rest else ""

    # Checks whether it's a search command first (for example yt cats)
    if command in SEARCH and argument:
        webbrowser.open(SEARCH[command] + argument)

    # If it's a shortcut (gh -> github)
    if command in SHORTCUTS:
        webbrowser.open(SHORTCUTS[command])

    if DEFAULT_PREFIX in SEARCH:
        webbrowser.open(SEARCH[DEFAULT_PREFIX] + text)

def on_enter(event=None):
    global history_number

    text = entry_input.get().strip() # Get text from the entry box
    if text:
        history.append(text)
        history_number = len(history)

    window.withdraw() 
    window.update()
    run_command(text)
    entry_input.delete(0, "end")

def moving_history(step: int):
    global history_number
    if not history: return
    
    history_number = max(1, min(len(history), history_number + step))
    entry_input.delete(0, "end")
    entry_input.insert(0, history[-history_number])

# Converts config format to pynput one
def replace_hotkey(hotkey: str):
    # Ensure clean pynput format: ctrl+alt+z -> <ctrl>+<alt>+z
    parts = hotkey.lower().split('+')
    formatted = []
    for p in parts:
        if p in ['ctrl', 'alt', 'shift', 'win']:
            formatted.append(f"<{p}>")
        else:
            formatted.append(p)
    return "+".join(formatted)

def start_hotkey():
    try:
        hk_string = replace_hotkey(HOTKEY)
        with kb.GlobalHotKeys({hk_string: focus_window}) as h:
            h.join()
    except Exception as e:
        print(f"Hotkey Error: {e}")

# Start listener
threading.Thread(target=start_hotkey, daemon=True).start()

window.bind("<Escape>", lambda e: window.withdraw())
entry_input.bind("<Return>", on_enter)
entry_input.bind("<Up>", lambda e: moving_history(1))
entry_input.bind("<Down>", lambda e: moving_history(-1))

window.mainloop()