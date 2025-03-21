import glob
import os
import platform
import queue
import subprocess
import threading
import time
import re 
import tkinter as tk
from tkinter import ttk

#Help Function for use not relevant for class 
command_args = {
        "Re-encode" : "--recode-video",
        "write-thumbnail":"--write-thumbnail",
        "write-all-thumbnails":"--write-all-thumbnails",
        "list-thumbnails":"--list-thumbnails ",
        "keep-video":"-k",
        "abort-on-error":"--abort-on-error",
        "dump-json": "-j",
        "write-subs": "--write-subs",
        "write-auto-subs":"--write-auto-subs",
        "M4A":"m4a",
        "MP4": "mp4",
        "FLV":"flv",
        "WAV": "wav",
        "OGG": "ogg",
        "MP3":"mp3",
        "WebM":"webm"
        }

def parse_download_output(output_text):
    # Define regex pattern to extract information
    pattern = r'\[download\]\s+(\d+\.\d+)% of\s+(\d+\.\d+\w+) at\s+(\d+\.\d+\w+/s|\d+\.\d+\w+) ETA (\d+:\d+)'
    
    # Find all matches in the output text
    matches = re.findall(pattern, output_text)
    
    results = []
    for match in matches:
        progress = float(match[0])
        size = match[1]
        speed = match[2]
        eta = match[3]
        
        results.append({
            'progress': progress,
            'size': size,
            'speed': speed,
            'eta': eta
        })
    
    return results

def get_latest_progress(output_text):
    results = parse_download_output(output_text)
    if results:
        return results[-1]
    return None

def unix_delete_part_files(directory_path):
    # Create a pattern to match all files ending with .part
    pattern = os.path.join(directory_path, "*.part")
    
    # Find all matching files
    part_files = glob.glob(pattern)
    
    # Count how many files we'll delete
    count = 0
    
    # Delete each file
    for file_path in part_files:
        try:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
            count += 1
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")
    
    print(f"Total files deleted: {count}")
    return count

def windows_delete_part_files(directory_path):
    # Count how many files we'll delete
    count = 0
    
    # Walk through all files in the directory
    for filename in os.listdir(directory_path):
        # Check if the file ends with .part
        if filename.endswith(".part"):
            file_path = os.path.join(directory_path, filename)
            
            # Make sure it's a file, not a directory
            if os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                    count += 1
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")
    
    print(f"Total files deleted: {count}")
    return count

class downlodad_with_cmd():
    
    def __init__(self,json_settings:dict,progress_bar:ttk.Progressbar=None):
        self.process = None
        self.path = json_settings["path"]
        command_parts = []
        self.progress_bar = progress_bar
        command_parts.append(".\\yt-dlp.exe")
        command_parts.append(json_settings["youtube_url"])
        command_parts.append(" ".join([command_args["Re-encode"], command_args[json_settings["file_formate"]]])) 
        command_parts.append(" ".join(["-P",json_settings["path"]]))
        
        for arg in list(json_settings)[2:]:
            if arg in list(command_args):
                command_parts.append(command_args[arg])
        
        self.command = " ".join(command_parts)
        print(self.command)
    def abort_process(self):
        if platform.system() == "Windows":
                print("Kill Prozess")
                subprocess.run(["taskkill", "/F", "/T", "/PID", str(self.process.pid)], capture_output=True)
                windows_delete_part_files(self.path)
        pass
    
    def run (self):
        process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, start_new_session=True,shell=True )
        self.process = process
        while True:
            output = process.stdout.readline()
            if(output == "" and process.poll() is not None):
                self.progress_bar["value"] = 0
                self.process =None
                break
            if output:
                latest = get_latest_progress(output)
                if latest is not None:
                    if self.progress_bar is not None:
                       self.progress_bar["value"] = latest['progress']
                    print(f"Progress: {latest['progress']}%, Speed: {latest['speed']}, ETA: {latest['eta']}")
        if process.returncode != 0:
            print(f"Command failed with error: {process.stderr.read()}")


class queue_download_with_cmd():
    
    def __init__(self):
        self.q = queue.Queue()
        self.isdownloading = False
        self.runable = None

    def put(self, run_able_objeckt: downlodad_with_cmd):
        self.q.put(run_able_objeckt)
        
    def abort_curent_prozess(self):
        print("mion")
        if  self.runable is not None:
            assert isinstance(self.runable, downlodad_with_cmd), "Queue item is not a valid instance"
            print("hallo")
            self.runable.abort_process()
                
    def start_download_able(self):
        def run_if_able():
            while True:
                if not self.q.empty():
                    while not self.q.empty():
                        self.isdownloading = True 
                        runable = self.q.get()
                        assert isinstance(runable, downlodad_with_cmd), "Queue item is not a valid instance"
                        self.runable = runable
                        runable.run()
                        self.isdownloading = False
                        self.runable = None
                        
                time.sleep(1)
        
        thread = threading.Thread(target=run_if_able, daemon=True)
        thread.start() 
    
   



if __name__ == "__main__":
   
    dic ={
        "youtube_url": "https://www.youtube.com/watch?v=T2FtOJnf9M8",
        "file_formate":"m4a"
    }
    dic2 ={
        "youtube_url": "https://www.youtube.com/watch?v=r9oeYna3F7Q",
        "file_formate":"m4a"
    }
    dic3 ={
        "youtube_url": "https://www.youtube.com/watch?v=QKyxxhqx7Xo",
        "file_formate":"m4a"
    }
    befehl = downlodad_with_cmd(dic)
    befehl2 = downlodad_with_cmd(dic2)
    befehl3 = downlodad_with_cmd(dic3)
    download_manager = queue_download_with_cmd()
    time.sleep(20)
    download_manager.start_download_able()
    download_manager.put(befehl)
    download_manager.put(befehl2)
    download_manager.put(befehl3)
    time.sleep(200)
   

   
   
    