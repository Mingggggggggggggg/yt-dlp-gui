# Einstellungen als Json im selben ordner speichern und laden
# So sollen benutzerdefinierte Standardeinstellungen eingestellt werden können
# Existiert die Datei nicht, wird diese erstellt, sonst lade aus der Datei
import json
import tkinter as tk
import os

def initialize():
    if not os.path.isdir("data"):
        os.mkdir("data")
    if  not os.path.exists("data/settings.json"):
        create_json({})

    
        

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

def create_json(dict_setting: dict):
    with open("data/settings.json", "w") as json_file:
        json.dump(dict_setting, json_file, indent=4)
    print("Set default settings.")


def load_settings(checkboxes, selected_format, path_var, filename="data/settings.json"):
    try:
        with open(filename, "r") as file:
            settings = json.load(file)

        if "checkboxes" in list(settings):
            for name, var in checkboxes:
                if name in settings["checkboxes"]:
                    var.set(settings["checkboxes"][name])

        if "selected_format" in list(settings):
            selected_format.set(settings["selected_format"])

        if "download_path" in list(settings):
            path_var.set(settings["download_path"])

        print("Settings loaded.")
    except FileNotFoundError:
        print("No settings found.")



def save_settings(checkboxes, selected_format, path_var, filename="data/settings.json"):
    settings = {
        "checkboxes": {name: var.get() for name, var in checkboxes},
        "selected_format": selected_format.get(),
        "download_path": path_var.get()
    }

    with open(filename, "w") as file:
        json.dump(settings, file, indent=4)

    print("Settings saved.")

