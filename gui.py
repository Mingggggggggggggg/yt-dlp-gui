import tkinter as tk
from tkinter import filedialog
import os
from tkinter import ttk
from cmd_command_use import downlodad_with_cmd, queue_download_with_cmd
from settings import create_dict_out_of_setting

class ToolTip:
    """ Klasse für Tooltip mit einstellbarer Verzögerung """
    def __init__(self, widget, text, delay=1000):  # 1 Sekunde Verzögerung
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.delay = delay
        self.after_id = None

        widget.bind("<Enter>", self.schedule_tooltip)
        widget.bind("<Leave>", self.cancel_tooltip)

    def schedule_tooltip(self, event=None):
        self.cancel_tooltip()
        self.after_id = self.widget.after(self.delay, self.show_tooltip)

    def cancel_tooltip(self, event=None):
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None
        self.hide_tooltip()

    def show_tooltip(self):
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip_window, text=self.text, bg="yellow", relief="solid", borderwidth=1, font=("Arial", 9))
        label.pack()

    def hide_tooltip(self):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


def select_download_path():
    """ Öffnet den Explorer, um einen Download-Pfad auszuwählen """
    path = filedialog.askdirectory()
    if path:
        path_var.set(path)  # Setzt das Label auf den gewählten Pfad


def start_gui():
    root = tk.Tk()
    root.title("YT-DLP GUI")
    root.geometry('700x500')
    root.resizable(False, False)

    # Standardpfad ist das Verzeichnis der ausführenden Datei
    default_path = os.path.dirname(os.path.abspath(__file__))

    # Eingabefeld für YouTube-Link
    input_frame = tk.Frame(root)
    input_frame.pack(pady=10)

    tk.Label(input_frame, text="YouTube-Link:", font=("Arial", 10)).pack(side='left')
    input_field = tk.Text(input_frame, height=1, width=50)
    input_field.pack(side='left', padx=5)

    def paste_from_clipboard():
        input_field.delete("1.0", tk.END)
        input_field.insert(tk.END, root.clipboard_get())

    tk.Button(input_frame, text="Paste", command=paste_from_clipboard).pack(side='left', padx=5)

    # Checkboxen
    checkbox_frame = tk.Frame(root)
    checkbox_frame.pack(pady=10)

    checkbox_categories = {
        "Quick Access": {
            "write-thumbnail": "Write thumbnail image to disk (default off)",
            "write-all-thumbnails": "Write all thumbnail image formats to disk",
            "list-thumbnails": "List available thumbnails of each video",
            "keep-video": "Originaldatei behalten",
            "postprocessor-args": "Zusätzliche Argumente für Post-Processing"
        },
        "Misc": {
            "abort-on-error": "Off by default",
            "dump-json": "Print JSON information for each video",
            "write-subs": "Write subtitle file (default off)",
            "write-auto-subs": "Write automatically generated subtitle file"
        }
    }

    checkboxes = []

    for category, options in checkbox_categories.items():
        tk.Label(checkbox_frame, text=category, font=("Arial", 10, "bold")).pack(anchor="w", pady=(5, 2))
        row_frame = tk.Frame(checkbox_frame)
        row_frame.pack()

        for name, tooltip_text in options.items():
            var = tk.BooleanVar()
            checkbox = tk.Checkbutton(row_frame, text=name, variable=var)
            checkbox.pack(side="left", padx=5)
            ToolTip(checkbox, tooltip_text, delay=1000)
            checkboxes.append(var)

    # Dropdown-Menü für Dateiformat
    dropdown_frame = tk.Frame(root)
    dropdown_frame.pack(pady=10)

    tk.Label(dropdown_frame, text="Select Fileformat:", font=("Arial", 10)).pack(side='left', padx=5)

    file_formats = {
        "M4A": "MPEG-4 Audio, Apple Audio File",
        "MP4": "Standard Videoformat",
        "FLV": "Flash Videoformat",
        "WAV": "Uncompressed Audioformat",
        "OGG": "Open Audioformat",
        "MP3": "Audioformat",
        "WebM": "Google Videoformat"
    }

    selected_format = tk.StringVar(root)
    selected_format.set(list(file_formats.keys())[0])  # Standardwert setzen

    dropdown_menu = tk.OptionMenu(dropdown_frame, selected_format, *file_formats.keys())
    dropdown_menu.pack(side='left', padx=5)
    ToolTip(dropdown_menu, "Wähle das gewünschte Dateiformat aus", delay=1000)

    # Download-Pfad
    path_frame = tk.Frame(root)
    path_frame.pack(pady=10)

    custom_path_var = tk.BooleanVar()
    path_var = tk.StringVar(value=default_path)  # Standard = Ordner der Datei

    def toggle_path_selection():
        """ Aktiviert/Deaktiviert den Button zur Pfadauswahl """
        path_button.config(state="normal" if custom_path_var.get() else "disabled")
        if not custom_path_var.get():
            path_var.set(default_path)  # Zurücksetzen auf Root-Ordner der Datei

    path_checkbox = tk.Checkbutton(path_frame, text="Custom Download Path", variable=custom_path_var, command=toggle_path_selection)
    path_checkbox.pack(side="left", padx=5)

    path_button = tk.Button(path_frame, text="Ordner auswählen", command=select_download_path, state="disabled")
    path_button.pack(side="left", padx=5)

    path_label = tk.Label(path_frame, textvariable=path_var, font=("Arial", 10))
    path_label.pack(side="left", padx=5)

    # Download-Mangement erstellen
    Download_Manger = queue_download_with_cmd()
    Download_Manger.start_download_able()

    def download():
        settings_dict = create_dict_out_of_setting(input_field, checkboxes, selected_format)
        runable = downlodad_with_cmd(settings_dict, download_progressbar)
        Download_Manger.put(runable)

    # Download-Button über den anderen Buttons
    download_button_frame = tk.Frame(root)
    download_button_frame.pack(side="bottom", pady=5, fill="x")

    download_button = tk.Button(download_button_frame, text="Download", font=("Arial", 10), width=15, command=download)
    download_button.pack(expand=True, padx=10)

    # Fortschrittsbalken unten über die gesamte Breite
    progressbar_frame = tk.Frame(root)
    progressbar_frame.pack(side="bottom", fill="x", padx=10, pady=5)

    download_progressbar = ttk.Progressbar(progressbar_frame, mode="determinate")
    download_progressbar.pack(fill="x", expand=True)

    # Download- und Abort-Buttons unten
    button_frame = tk.Frame(root)
    button_frame.pack(side="bottom", pady=10, fill="x")

    abort_button = tk.Button(button_frame, text="Abort", font=("Arial", 10), width=15)
    abort_button.pack(side="right", expand=True, padx=10)

    root.mainloop()


if __name__ == "__main__":
    start_gui()
