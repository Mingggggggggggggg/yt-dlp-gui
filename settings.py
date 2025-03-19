# Einstellungen als Json im selben ordner speichern und laden
# So sollen benutzerdefinierte Standardeinstellungen eingestellt werden können
# Existiert die Datei nicht, wird diese erstellt, sonst lade aus der Datei
import tkinter as tk

def initialize():
    pass

def create_json(input_flied:tk.Text):
    {
        "youtube_url" : input_flied.get(0,tk.END).strip(),
    }

def load_json():
    pass