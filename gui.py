# Zeit drangesessen: 3h
import tkinter as tk

class ToolTip:
    """ Klasse für Tooltip mit einstellbarer Verzögerung """
    def __init__(self, widget, text, delay=100):  # Delay in Millisekunden (Standard 1 Sekunde)
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.delay = delay
        self.after_id = None

        # Event-Bindings für Mausbewegungen
        widget.bind("<Enter>", self.schedule_tooltip)
        widget.bind("<Leave>", self.cancel_tooltip)

    def schedule_tooltip(self, event=None):
        """ Starte Timer für Tooltip-Verzögerung """
        self.cancel_tooltip()  # Falls schon ein alter Timer läuft, abbrechen
        self.after_id = self.widget.after(self.delay, self.show_tooltip)

    def cancel_tooltip(self, event=None):
        """ Stoppt den Timer und entfernt Tooltip, falls sichtbar """
        if self.after_id:
            self.widget.after_cancel(self.after_id)  # Timer abbrechen
            self.after_id = None
        self.hide_tooltip()

    def show_tooltip(self):
        """ Tooltip anzeigen, wenn der Timer abgelaufen ist """
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip_window, text=self.text, bg="yellow", relief="solid", borderwidth=1, font=("Arial", 9))
        label.pack()

    def hide_tooltip(self):
        """ Tooltip ausblenden """
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


def start_gui():
    root = tk.Tk()
    root.title("YT-DLP GUI")
    root.geometry('700x400')
    root.resizable(False, False)

    input_frame = tk.Frame(root)
    input_frame.pack(pady=10)

    # Beschriftung für das Eingabefeld
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

    # Kategorien mit Überschriften und Tooltips
    checkbox_categories = {
        "Quick Access": {
            "recode-video": " Re-encode the video into another format if necessary this includes audio formats",
            "[Entfernt]": " Convert video files to audio-only files",
            "write-thumbnail": "DEFAULT:  Do not write thumbnail image to disk",
            "write-all-thumbnails": "Write all thumbnail image formats to disk",
            "list-thumbnails": "List available thumbnails of each video",
            "keep-video": "Keep the intermediate video file on disk after post-processing"
        },
        "Post-Processing Options": {
            "audio-format": "Standard-Videoformat, weit verbreitet", # Separates Dropdown
            "audio-quality": "Hochwertiges Videoformat mit mehreren Streams", # Dropdown
            "postprocessor-args": "Für Web-Streaming optimiertes Format", # Dropdown
            "PL1": "Flash-Videoformat",
            "PL2": "Altes Format für Mobiltelefone",
            "PL3": "Älteres Videoformat mit guter Qualität"
        },
        "PLAYLIST KRAM HIER": {
            "PL4": "Erzwingt eine Konvertierung des Videos",
            "PL5": "Lädt nur das Video herunter",
            "PL6": "Lädt verfügbare Untertitel herunter",
            "PL7": "Lädt nur die Audiospur herunter",
            "PL8": "Platzhalter-Option B",
            "PL9": "Platzhalter-Option C"
        }
    }

    checkboxes = []

    for category, options in checkbox_categories.items():
        # Überschrift für die Kategorie
        label = tk.Label(checkbox_frame, text=category, font=("Arial", 10, "bold"))
        label.pack(anchor="w", pady=(5, 2))

        row_frame = tk.Frame(checkbox_frame)
        row_frame.pack()

        for name, tooltip_text in options.items():
            var = tk.BooleanVar()
            checkbox = tk.Checkbutton(row_frame, text=name, variable=var)
            checkbox.pack(side="left", padx=5)
            ToolTip(checkbox, tooltip_text, delay=1000)  # Tooltip erscheint nach 1 Sekunde
            checkboxes.append(var)

    # Frame für das Dropdown-Menü
    dropdown_frame = tk.Frame(root)
    dropdown_frame.pack(pady=10)

    # Label für das Dropdown
    dropdown_label = tk.Label(dropdown_frame, text="Dateiformat auswählen:", font=("Arial", 10))
    dropdown_label.pack(side='left', padx=5)

    # Optionen für das Dropdown-Menü
    file_formats = {
        "M4A": "Audioformat von Apple",
        "MP4": "Standard-Videoformat",
        "FLV": "Flash Videoformat",
        "WAV": "Unkomprimiertes Audioformat",
        "OGG": "Offenes Audioformat",
        "MP3": "Beliebtes Audioformat",
        "WebM": "Google Videoformat"
    }

    selected_format = tk.StringVar(root)
    selected_format.set(list(file_formats.keys())[0])  # Standardwert setzen

    # Dropdown-Menü erstellen
    dropdown_menu = tk.OptionMenu(dropdown_frame, selected_format, *file_formats.keys())
    dropdown_menu.pack(side='left', padx=5)
    ToolTip(dropdown_menu, "Wähle das gewünschte Dateiformat aus", delay=1000)  # Tooltip mit Verzögerung

    root.mainloop()

if __name__ == "__main__":
    start_gui()
