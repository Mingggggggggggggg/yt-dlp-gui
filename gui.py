import tkinter as tk
from tkinter import filedialog
import os
from tkinter import ttk
from cmd_command_use import downlodad_with_cmd, queue_download_with_cmd
from settings import create_dict_out_of_setting, save_settings, load_settings



class ToolTip:
    def __init__(self, widget, text, delay=1000):
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


def start_gui():
    root = tk.Tk()
    root.title("YT-DLP GUI")
    root.geometry('900x500')
    root.resizable(False, False)


    toolbar = tk.Frame(root, height=40)
    toolbar.pack(side=tk.TOP, fill=tk.X)
    toolbar.pack_propagate(False)

    sidebar_visible = tk.BooleanVar(value=False)

    def toggle_sidebar():
        if sidebar_visible.get():
            sidebar.pack_forget()
            sidebar_toggle_btn.config(text="▶ Show Downloads")
            sidebar_visible.set(False)
        else:
            sidebar.pack(side=tk.LEFT, fill=tk.Y,padx=5)
            sidebar_toggle_btn.config(text="◀ Hide Downloads")
            sidebar_visible.set(True)
    
    sidebar_toggle_btn = tk.Button(
    toolbar, 
    text="▶ Show Downloads", 
    command=toggle_sidebar
    )
    sidebar_toggle_btn.pack(side=tk.LEFT, padx=5, pady=5) 
    sidebar = tk.Frame(root, width=300)
    sidebar.pack_propagate(False)
    

    # Sidebar downloads container
    downloads_container = tk.Frame(sidebar, bg='lightgray')
    downloads_container.pack(fill=tk.BOTH, expand=False)

    # Main content frame
    main_content = tk.Frame(root)
    main_content.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
    
    default_path = os.path.dirname(os.getcwd())

    input_frame = tk.Frame(main_content)
    input_frame.pack(pady=10)

    tk.Label(input_frame, text="YouTube-Link:", font=("Arial", 10)).pack(side='left')
    input_field = tk.Text(input_frame, height=1, width=50)
    input_field.pack(side='left', padx=5)

    def paste_from_clipboard():
        input_field.delete("1.0", tk.END)
        input_field.insert(tk.END, root.clipboard_get())

    tk.Button(input_frame, text="Paste", command=paste_from_clipboard).pack(side='left', padx=5)
    
    checkbox_frame = tk.Frame(main_content)
    checkbox_frame.pack(pady=10)

    checkbox_categories = {
        "Quick Access": {
            "write-thumbnail": "Write thumbnail image to disk (default off)",
            "write-all-thumbnails": "Write all thumbnail image formats to disk",
            "list-thumbnails": "List available thumbnails of each video",
            "keep-video": "Originaldatei behalten",
            "no-parts": "Don't create a part File at Downloading"
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
            checkboxes.append((name, var))

    dropdown_frame = tk.Frame(main_content)
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
    selected_format.set(list(file_formats.keys())[0])

    dropdown_menu = tk.OptionMenu(dropdown_frame, selected_format, *file_formats.keys())
    dropdown_menu.pack(side='left', padx=5)
    ToolTip(dropdown_menu, "Select Fileformat", delay=1000)

    path_frame = tk.Frame(main_content)
    path_frame.pack(pady=10)

    custom_path_var = tk.BooleanVar()
    path_var = tk.StringVar(value=default_path)

    def toggle_path_selection():
        path_button.config(state="normal" if custom_path_var.get() else "disabled")
        if not custom_path_var.get():
            path_var.set(default_path)
    
    def select_download_path():
        path = filedialog.askdirectory()
        if path:
            path_var.set(path)
            
    path_checkbox = tk.Checkbutton(path_frame, text="Custom Download Path", variable=custom_path_var, command=toggle_path_selection)
    path_checkbox.pack(side="left", padx=5)

    path_button = tk.Button(path_frame, text="Select Folder", command=select_download_path, state="disabled")
    path_button.pack(side="left", padx=5)

    path_label = tk.Label(path_frame, textvariable=path_var, font=("Arial", 10))
    path_label.pack(side="left", padx=5)

   
    Download_Manger = queue_download_with_cmd()
    Download_Manger.start_download_able()

    load_settings(checkboxes, selected_format, path_var)

    def download():
        download_frame = tk.Frame(downloads_container,bg='lightgray')
        download_frame.pack(fill=tk.X,padx=5,pady=5)
        # Filename label
        filename_label = tk.Label(download_frame,text= "haloo", bg='lightgray')
        filename_label.pack(anchor='w')
        # Progress bar
        progress = ttk.Progressbar(download_frame, length=200, mode='determinate')
        progress.pack(fill=tk.X, pady=2)

        # Speed label
        speed_label = tk.Label(download_frame, text="0 KB/s", bg='lightgray')
        speed_label.pack(anchor='w')
        
        #Abort Button 
        abort_button = tk.Button(download_frame, text="Abort", font=("Arial", 8), width=10)
        abort_button.pack(anchor='e', pady=2)
        
        settings_dict = create_dict_out_of_setting(input_field, checkboxes, selected_format, path_var)
        runable = downlodad_with_cmd(settings_dict,Download_Manger, progress,filename_label,speed_label,abort_button)
        Download_Manger.put(runable)
        Download_Manger.append(runable,download_frame)
        

        
    """
    progressbar_frame = tk.Frame(main_content)
    progressbar_frame.pack(side="bottom", fill="x", padx=10, pady=5)

    download_progressbar = ttk.Progressbar(progressbar_frame, mode="determinate")
    download_progressbar.pack(fill="x", expand=True)
    """
    button_frame = tk.Frame(main_content)
    button_frame.pack(side="bottom", pady=10, fill="x")
    
    download_button = tk.Button(button_frame, text="Download", font=("Arial", 10), width=15, command=download)
    download_button.pack(side="left", expand=True, padx=10)
    """
    abort_button = tk.Button(button_frame, text="Abort", font=("Arial", 10), width=15, command=Download_Manger.abort_curent_prozess)
    abort_button.pack(side="right", expand=True, padx=10)
    """
    def on_closing():
        save_settings(checkboxes, selected_format,custom_path_var, path_var)
        root.destroy()


    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    
    root.mainloop()



if __name__ == "__main__":
    start_gui()