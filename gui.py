import tkinter as tk

def start_gui():
    root = tk.Tk()
    root.title("YT-DLP GUI")
    root.geometry('550x350')  # Höhe auf 350 erhöht wegen Dropdown
    root.resizable(False, False)

    input_frame = tk.Frame(root)
    input_frame.pack(pady=10)

    # Beschriftung links neben dem Eingabefeld
    input_label = tk.Label(input_frame, text="YouTube-Link:", font=("Arial", 10))
    input_label.pack(side='left')

    # Eingabefeld
    input_field = tk.Text(input_frame, height=1, width=50)
    input_field.pack(side='left', padx=5)

    # Funktion zum Einfügen aus der Zwischenablage
    def paste_from_clipboard():
        input_field.delete("1.0", tk.END)
        input_field.insert(tk.END, root.clipboard_get())

    # Paste-Button
    paste_button = tk.Button(input_frame, text="Paste", command=paste_from_clipboard)
    paste_button.pack(side='left', padx=5)

    # Frame für Checkboxen
    checkbox_frame = tk.Frame(root)
    checkbox_frame.pack(pady=10)

    # Eigene Namen für die Checkboxen
    checkbox_names = [
        "Audio", "Video", "Untertitel", "1080p", "720p", 
        "480p", "MP4", "MKV", "WebM", "Null"
    ]

    checkboxes = []
    for i in range(5):  # Y Achse
        for j in range(2):  # X Achse
            var = tk.BooleanVar()
            checkbox = tk.Checkbutton(checkbox_frame, text=checkbox_names[i + j], variable=var)
            checkbox.grid(row=j, column=i, padx=5, pady=5)
            checkboxes.append(var)  # Falls du später die Werte abrufen willst

    # Frame für das Dropdown-Menü
    dropdown_frame = tk.Frame(root)
    dropdown_frame.pack(pady=10)

    # Label für das Dropdown
    dropdown_label = tk.Label(dropdown_frame, text="Dateiformat auswählen:", font=("Arial", 10))
    dropdown_label.pack(side='left', padx=5)

    # Optionen für das Dropdown-Menü
    file_formats = ["MP4", "MKV", "WebM", "MP3", "AAC", "FLAC", "WAV"]
    selected_format = tk.StringVar(root)
    selected_format.set(file_formats[0])  # Standardwert setzen

    # Dropdown-Menü
    dropdown_menu = tk.OptionMenu(dropdown_frame, selected_format, *file_formats)
    dropdown_menu.pack(side='left', padx=5)

    root.mainloop()

if __name__ == "__main__":
    start_gui()
