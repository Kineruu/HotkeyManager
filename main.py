import customtkinter as ct
import webbrowser
import threading
import keyboard

"""
TODO:
-> JSON config so so I don't end up with 50 if and elses

"""

window = ct.CTk()
window.geometry("90x30")
window.resizable(False, False)
window.overrideredirect(True)
frame = ct.CTkFrame(master=window)
frame.pack()

entry_input = ct.CTkEntry(frame, width=80, height=25)
entry_input.pack(side="left")

def close_window():
    window.withdraw()

close_button = ct.CTkButton(frame, width=5, height=10, command=close_window, text="x")
close_button.pack(side="left")

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

    if text == "gh":
        webbrowser.open("https://github.com")

    elif text == "yt":
        webbrowser.open("https://www.youtube.com/")

    elif text.startswith("yt "):
        search = text[3:]
        url = f"https://www.youtube.com/results?search_query={search}"
        webbrowser.open(url)

    elif text.startswith("g "):
        search = text[2:]
        webbrowser.open(f"https://www.google.com/search?q={search}")

    entry_input.delete(0, "end")
    window.withdraw()
    
entry_input.bind("<Return>", keyboard_listener)

def start_listening():
    keyboard.add_hotkey(keys, show_window)
    keyboard.wait()

threading.Thread(target=start_listening, daemon=True).start()

window.mainloop()