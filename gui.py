import tkinter as tk
from tkinter import filedialog
import os

def start_gui():
    # Hauptfenster erstellen
    root = tk.Tk()
    root.title("YT-DLP GUI")
    root.geometry('600x300')
    root.maxsize(600, 300)

    # Standardpfad auf das aktuelle Verzeichnis setzen
    project_dir = os.getcwd()

    # Funktion zum Öffnen des Datei-Explorers und Anzeigen des Pfads
    def open_file_explorer():
        folder_selected = filedialog.askdirectory(initialdir=project_dir, title="Wähle einen Ordner")
        if folder_selected:  # Falls ein Ordner ausgewählt wurde
            path_label.config(text=folder_selected)

    # Rahmen für Ordnerauswahl
    folder_frame = tk.Frame(root)
    folder_frame.pack(anchor='w', padx=10, pady=5, fill='x')
    
    # Überschrift für Ordnerauswahl mit größerer Schrift
    folder_label = tk.Label(folder_frame, text="Ordner auswählen:", font=("Arial", 12, "bold"))
    folder_label.pack(anchor='w')
    
    # Unterrahmen für Button und Pfad
    path_frame = tk.Frame(folder_frame)
    path_frame.pack(anchor='w', fill='x', pady=2)
    
    # Button für Datei-Explorer
    explorer_button = tk.Button(path_frame, text="Ordner auswählen", command=open_file_explorer)
    explorer_button.pack(side='left', padx=5)
    
    # Label zur Anzeige des ausgewählten Pfads (rechts vom Button), standardmäßig mit Root-Verzeichnis
    path_label = tk.Label(path_frame, text=project_dir, anchor='w')
    path_label.pack(side='left', fill='x', expand=True)
    
    # Überschrift für das Eingabefeld mit größerer Schrift
    input_label = tk.Label(root, text="Youtube Link:", font=("Arial", 12, "bold"))
    input_label.pack(anchor='w', padx=10, pady=5)
    
    # Eingabefeld (links ausgerichtet)
    input_field = tk.Text(root, height=1, width=50)
    input_field.pack(anchor='w', padx=10, pady=10)

    # Hauptloop starten
    root.mainloop()

if __name__ == "__main__":
    start_gui()