
import customtkinter as ct
import json

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

def save_config(data):
    with open("config.json", "w") as f:
        return json.dump(data, f, indent=4)

def open_settings_window(parent=None):
    config = load_config()
    entries = {}

    settings_window = ct.CTkToplevel(parent)
    settings_window.title("Settings")
    settings_window.resizable(True, False)
    settings_window.geometry("400x350")

    settings_frame = ct.CTkScrollableFrame(settings_window)
    settings_frame.pack(expand=True, fill="both", padx=10, pady=(10, 0))

    for key, value in config.items():

        section_row = ct.CTkFrame(settings_frame)
        section_row.pack(fill="x", pady=(10, 2))

        section_label = ct.CTkLabel(section_row, text=key, font=("Arial", 14, "bold"))
        section_label.pack(side="left")

        if isinstance(value, dict):
            add_button = ct.CTkButton(section_row, text="+", width=25)
            add_button.pack(side="right")
            
        if isinstance(value, dict):
            entries[key] = {}

            for sub_key, sub_value in value.items():
                row = ct.CTkFrame(settings_frame)
                row.pack(fill="x", pady=2)

                row.grid_columnconfigure(0, weight=1)
                row.grid_columnconfigure(1, weight=0)
                row.grid_columnconfigure(2, weight=1)

                sub_key_entry = ct.CTkEntry(row)
                sub_key_entry.insert(0, str(sub_key))
                sub_key_entry.grid(row=0, column=0, sticky="ew", padx=5)

                label = ct.CTkLabel(row, text=":")
                label.grid(row=0, column=1)

                sub_value_entry = ct.CTkEntry(row)
                sub_value_entry.insert(0, str(sub_value))
                sub_value_entry.grid(row=0, column=2, sticky="ew", padx=5)

                entries[key][sub_key] = (sub_key_entry, sub_value_entry)

        else:
            row = ct.CTkFrame(settings_frame)
            row.pack(fill="x", pady=2)

            entry = ct.CTkEntry(row)
            entry.insert(0, str(value))
            entry.pack(side="right", fill="x", expand=True)

            entries[key] = entry

    def on_save():
        new_config = {}

        for key, value in entries.items():
            if isinstance(value, dict):
                new_config[key] = {}

                for _, (key_entry, val_entry) in value.items():
                    new_key = key_entry.get()
                    new_val = val_entry.get()

                    new_config[key][new_key] = new_val
            else:
                new_config[key] = value.get()

        save_config(new_config)
        settings_window.destroy()

    save_button = ct.CTkButton(settings_window, text="SAVE", command=on_save)
    save_button.pack(pady=10)
