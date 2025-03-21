# Einstellungen als Json im selben ordner speichern und laden
# So sollen benutzerdefinierte Standardeinstellungen eingestellt werden können
# Existiert die Datei nicht, wird diese erstellt, sonst lade aus der Datei
import json
import tkinter as tk

def initialize():
    pass

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

def load_json():
    pass