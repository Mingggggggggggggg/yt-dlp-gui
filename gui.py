import tkinter as tk
import os

def start_gui():
    # Hauptfenster erstellen
    root = tk.Tk()
    root.title("YT-DLP GUI")
    root.geometry('600x300')
    root.maxsize(600, 300)

    
    # Überschrift für das Eingabefeld mit größerer Schrift
    input_label = tk.Label(root, text="Eingabefeld:", font=("Arial", 12, "bold"))
    input_label.pack(anchor='w', padx=10, pady=5)
    
    # Eingabefeld (links ausgerichtet)
    input_field = tk.Text(root, height=1, width=50)
    input_field.pack(anchor='w', padx=10, pady=10)

    # Hauptloop starten
    root.mainloop()

if __name__ == "__main__":
    start_gui()
