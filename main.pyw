
# Imports
from pynput import keyboard as kb 
from PIL import Image
import win32gui, win32con, win32api, win32process
import webbrowser, threading, json, os, pystray, sys, traceback, datetime
import customtkinter as ct

BASE_PATH = os.path.dirname(os.path.abspath(sys.argv[0]))
LOG_DIR = os.path.join(BASE_PATH, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

def log_error(t="ERROR", exc=None):
    path = os.path.join(LOG_DIR, "error.log")

    with open(path, "a", encoding="utf-8") as f:
        f.write("\n" + "=" * 60 + "\n")
        f.write(f"[{datetime.datetime.now()}] {t}\n")
        if exc:
            f.write("".join(traceback.format_exception(type(exc), exc, exc.__traceback__)))
        else:
            f.write("No exception provided")

def global_error_handler(exc_type, exc_value, exc_traceback):
    path = os.path.join(LOG_DIR, "crash.log")
    with open(path, "a", encoding="utf-8") as f:
        f.write("\n" + "=-" * 40 + "\n")
        f.write(f"[{datetime.datetime.now()}] CRASH\n")
        traceback.print_exception(exc_type, exc_value, exc_traceback, file=f)
sys.excepthook = global_error_handler

def load_config():
    # Loading config
    with open(os.path.join(BASE_PATH, "config.json"), "r") as f: 
        return json.load(f)

def safe_run(t, func):
    try:
        return func()
    except Exception as e:
        log_error(t, e)

history = []
history_number = 0
running = True
hotkey_listener = None

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

def load_settings():
    import settings_window
    settings_window.open_settings_window(callback=start_hotkey)

# Settings button
settings_button = ct.CTkButton(frame, text="s", width=20, height=20, command=load_settings, fg_color="transparent", hover_color="#333333")
settings_button.pack(side="left", fill="both", expand=True, padx=(6, 2), pady=6)

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

# Quit menu
def quit_window(icon, item):
    # .stop() stops the pystray thread
    if icon: icon.stop()
    window.after(0, window.destroy)
    # Hard killing the entire thing
    os._exit(0)

# The small icon in the hidden icons place
def small_icon():
    # Creating a small square
    image = Image.open(os.path.join(BASE_PATH, "icon.ico"))
    # Right clicking the icon, will give a quit menu option
    menu = pystray.Menu(pystray.MenuItem('Quit', quit_window))
    icon = pystray.Icon("HotkeyManager", image, "Hotkey Manager", menu)
    icon.run()

def focus_window_logic():
    # 1. Reveals window
    window.deiconify()
    
    # Grabbing the window's id that Windows assigned to my CTk
    my_hwnd = window.winfo_id() 
    # Asks windows what window is the user looking at right now
    fore_hwnd = win32gui.GetForegroundWindow()
    # Gets the thread ID the python script is running in
    thread_it = win32api.GetCurrentThreadId()
    # Thread ID of the currently focused window
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
    
    window.update_idletasks()
    window.update()
    # 4. Force Topmost briefly
    window.attributes("-topmost", True)
    
    # 5. Force Keyboard Focus
    entry_input.focus_force()
    entry_input.delete(0, "end")
    entry_input.select_range(0, "end")
    
    # 6. Release Topmost so it doesn't stay stuck
    window.after(200, lambda: window.attributes("-topmost", False))

def focus_window(): 
    window.after(0, focus_window_logic)

# Focus window by process ID
def focus_window_by_pid(pid):
    def callback(hwnd, _):
        # Gets the thread ID
        _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
        # If PID matches and the window is visible
        if found_pid == pid and win32gui.IsWindowVisible(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
            # Stops searching
            return False 
        return True
    win32gui.EnumWindows(callback, None)

def run_command(text: str):
    config = load_config()

    SEARCH = config["SEARCH"]
    SHORTCUTS = config["SHORTCUTS"]
    FOLDERS = config["FILES"]
    DEFAULT_PREFIX = config["DEFAULT_PREFIX"]

    if not text: 
        return
    
    command, *rest = text.split(" ", 1)
    argument = rest[0] if rest else ""

    if command in FOLDERS:
        folder_path = FOLDERS[command]
        if os.path.exists(folder_path): os.startfile(folder_path)
        return

    # Checks whether it's a search command first (for example yt cats)
    if command in SEARCH and argument: 
        webbrowser.open(SEARCH[command] + argument)

    # If it's a shortcut (gh -> github)
    elif command in SHORTCUTS: 
        webbrowser.open(SHORTCUTS[command])

    elif DEFAULT_PREFIX in SEARCH: 
        webbrowser.open(SEARCH[DEFAULT_PREFIX] + text)

def run(text): 
    window.withdraw() 
    run_command(text)

def on_enter(event=None):
    global history_number

    text = entry_input.get().strip() # Get text from the entry box
    entry_input.delete(0, "end")
    if text:
        history.append(text)
        history_number = len(history)
    window.after(1, lambda: safe_run("COMMAND", lambda: run(text)))

    return "break"

def moving_history(step: int):
    global history_number
    if not history: 
        return
    
    history_number = max(1, min(len(history), history_number + step))
    entry_input.delete(0, "end")
    entry_input.insert(0, history[-history_number])

# Converts config format to pynput one
# Long list incoming...
def replace_hotkey(hotkey: str):
    modifiers = {"ctrl", "alt", "shift", "win"}

    special_keys = {
        "home": "<home>",
        "end": "<end>",
        "page up": "<page_up>",
        "page down": "<page_down>",
        "insert": "<insert>",
        "delete": "<delete>",

        # Numpad
        "num0": "<num0>",
        "num1": "<num1>",
        "num2": "<num2>",
        "num3": "<num3>",
        "num4": "<num4>",
        "num5": "<num5>",
        "num6": "<num6>",
        "num7": "<num7>",
        "num8": "<num8>",
        "num9": "<num9>",

        "num+": "<num_add>",
        "num-": "<num_subtract>",
        "num*": "<num_multiply>",
        "num/": "<num_divide>",
    }

    # Ensure clean pynput format: ctrl+alt+z -> <ctrl>+<alt>+z
    hotkey = hotkey.lower().replace("_", " ").strip()
    parts = hotkey.lower().split('+')
    formatted = []
    for p in parts:
        p = p.strip()

        if p in modifiers:
            formatted.append(f"<{p}>")
        elif p in special_keys:
            formatted.append(special_keys[p])
        else:
            formatted.append(p)
    return "+".join(formatted)

def start_hotkey():
    global hotkey_listener
    try:
        if hotkey_listener:
            hotkey_listener.stop()

        config = load_config()
        HOTKEY = config["HOTKEY"]
        MAPPED_HOTKEYS = config["MAPPED_HOTKEYS"]

        main_hotkey = replace_hotkey(HOTKEY)
        hotkey_map = {}
        hotkey_map[main_hotkey] = focus_window

        for hotkey, command in MAPPED_HOTKEYS.items():
            formatted_hotkey = replace_hotkey(hotkey)
            hotkey_map[formatted_hotkey] = lambda cmd = command: run_command(cmd)

        hotkey_listener = kb.GlobalHotKeys(hotkey_map)
        hotkey_listener.start()

    except Exception as e:
        log_error(f"HOTKEY FAILED: {e}")

window.bind("<Escape>", lambda e: window.withdraw())
entry_input.bind("<Return>", on_enter)
entry_input.bind("<Up>", lambda e: moving_history(1))
entry_input.bind("<Down>", lambda e: moving_history(-1))

if __name__ == "__main__":
    safe_run("HOTKEY SYSTEM", start_hotkey)
    threading.Thread(target=lambda: safe_run("TRAY ICON", small_icon), daemon=True).start()
    
    window.protocol("WM_DELETE_WINDOW", lambda: quit_window(None, None))
    try: 
        window.mainloop()
    except KeyboardInterrupt: 
        os._exit(0)
    