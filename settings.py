# Einstellungen als Json im selben ordner speichern und laden
# So sollen benutzerdefinierte Standardeinstellungen eingestellt werden können
# Existiert die Datei nicht, wird diese erstellt, sonst lade aus der Datei
import json
import tkinter as tk
import os

def initialize():
    if os.path.exists("settings.json"):
        load_settings()
    else:
        create_json()


def create_dict_out_of_setting(input_flied:tk.Text,checkboxes:list,file_formate:tk.StringVar,real_path:tk.StringVar):
    json_dict = {
        "youtube_url" : input_flied.get("1.0",tk.END).strip()
    }
    json_dict["file_formate"] = file_formate.get()
    json_dict["path"] = real_path.get()
    for checkbox in checkboxes:
        if checkbox[1].get():
            json_dict[checkbox[0]] = checkbox[1].get()
    return json_dict

def create_json(dict_setting:dict):
    with open("settings.json", "w") as json_file:
        json.dump(dict_setting, json_file, indent=4)


def load_settings(checkboxes, selected_format, path_var, filename="settings.json"):
    try:
        with open(filename, "r") as file:
            settings = json.load(file)

        # Checkbox-Werte setzen
        for name, var in checkboxes:
            if name in settings["checkboxes"]:
                var.set(settings["checkboxes"][name])

        # Dropdown-Wert setzen
        selected_format.set(settings["selected_format"])

        # Pfad setzen
        path_var.set(settings["download_path"])

        print("Einstellungen geladen.")
    except FileNotFoundError:
        print("Keine gespeicherten Einstellungen gefunden.")


def save_settings(checkboxes, selected_format, path_var, filename="settings.json"):
    settings = {
        "checkboxes": {name: var.get() for name, var in checkboxes},
        "selected_format": selected_format.get(),
        "download_path": path_var.get()
    }

    with open(filename, "w") as file:
        json.dump(settings, file, indent=4)

    print("Einstellungen gespeichert.")

