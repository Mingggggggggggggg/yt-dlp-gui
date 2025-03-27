import glob
import os
import platform
import queue
import signal
import subprocess
import sys
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
        "no-parts":"--no-part",
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


def unix_delete_files_starting_with(directory_path, prefix):
    time.sleep(1)
    # Create pattern to match files starting with prefix
    pattern = os.path.join(directory_path, f"{prefix}*")
    
    # Find all matching files
    matching_files = glob.glob(pattern)
    
    count = 0
    # Delete each matched file
    for file_path in matching_files:
        try:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
            count += 1
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")
    
    print(f"Total files deleted: {count}")
    return count

def windows_delete_files_starting_with(directory_path, prefix):
    time.sleep(1)
    count = 0
    
    # Check all files in directory
    for filename in os.listdir(directory_path):
        # Match files starting with prefix
        if filename.startswith(prefix):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                    count += 1
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")
    
    print(f"Total files deleted: {count}")
    return count

def unix_delete_part_files(directory_path):
    # Create a pattern to match all files ending with .part
    time.sleep(1)
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
    time.sleep(1)
    count = 0
    print(os.listdir(directory_path))
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

def updater():
    process = subprocess.Popen(".\\yt-dlp.exe -U", stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, start_new_session=True,shell=True )
    while True:
        output = process.stdout.readline()
        if(output == "" and process.poll() is not None):
             break
        if output:
            print(output)
    process.wait()

class downlodad_with_cmd():
    
    def __init__(self,json_settings:dict,download_manager,progress_bar:ttk.Progressbar=None,file_name_label:tk.Label=None,speed_label:tk.Label= None,abort_button:tk.Button= None):
        #Download Manager to remove the download form List
        self.download_manager = download_manager
        #Command for the Titel of the UI Elements 
        self.get_title_command = f".\\yt-dlp.exe -e --no-warnings  {json_settings["youtube_url"]}"
        self.process = None
        self.path = json_settings["path"]
        command_parts = []
        command_parts.append(".\\yt-dlp.exe")
        command_parts.append(json_settings["youtube_url"])
        command_parts.append(" ".join([command_args["Re-encode"], command_args[json_settings["file_formate"]]])) 
        command_parts.append(" ".join(["-P",'"',json_settings["path"],'"']))
        
        for arg in list(json_settings)[2:]:
            if arg in list(command_args):
                command_parts.append(command_args[arg])
        
        self.command = " ".join(command_parts)
        print(self.command)
        """
           ↑  ↑   ↑
        In this Part the command and more Logical parts are declart 

            
        In this Part the UI Elememnts are delcaret 
          ↓  ↓  ↓
        """
        #TODO Add Threadinding for for Label Call to not Frezeze UI Thread 
        self.isDelete = False
        self.progress_bar = progress_bar
        self.file_name_label = file_name_label
        self .speed_label = speed_label
        if abort_button is not None:
            abort_button.config(command=self.abort_self)
        self.name_label("DEFAULT NAME")
        t = threading.Thread(target= self.name_label_form_url,daemon= True)
        t.start()
       
    
    def name_label_form_url(self):
        process = subprocess.Popen(
            self.get_title_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True
        )
        stdout, stderr = process.communicate()
        if self.progress_bar is not None:
            self.file_name_label["text"] = stdout.strip()

    def name_label(self,label):
        if self.progress_bar is not None:
            self.file_name_label["text"] = label

    
    def update_progressbar(self,update_value):
        if self.progress_bar is not None and not self.isDelete:
            self.progress_bar["value"] = update_value
        
    def update_speed_label(self,update_speed):
        if self.speed_label is not None and not self.isDelete:
            self.speed_label["text"] = update_speed
    
    def abort_process(self):
        self.isDelete = True
        if platform.system() == "Windows":
                subprocess.run(["taskkill", "/F", "/T", "/PID", str(self.process.pid)], capture_output=True)
                windows_delete_part_files(self.path)
                if self.file_name_label is not None:
                    windows_delete_files_starting_with(self.path,self.file_name_label["text"])
        else:
            try:
            # Get the process group ID (works if process was started with start_new_session=True)
                pgid = os.getpgid(self.process.pid)
            
            # Send SIGTERM to entire process group
                os.killpg(pgid, signal.SIGTERM)
            
            # Wait for graceful termination
                deadline = time.time() + 2
                while time.time() < deadline and self.process.poll() is None:
                    time.sleep(0.1)
            
            # Force kill if still running
                if self.process.poll() is None:
                    os.killpg(pgid, signal.SIGKILL)
                
            # Ensure we reap the process status
                self.process.wait()
                unix_delete_part_files(self.path)
                unix_delete_files_starting_with(self.path,self.file_name_label["text"])
            except ProcessLookupError:
            # Process already dead
             pass
            except PermissionError as e:
                print(f"Permission denied: {e}", file=sys.stderr)
                self.process.kill()
            except Exception as e:
                print(f"Unexpected error: {e}", file=sys.stderr)
                self.process.kill()

    def abort_self(self):
        self.download_manager.abort_or_remove(self)

    
    def run (self):
        process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, start_new_session=True,shell=True )
        self.process = process
        while True:
            output = process.stdout.readline()
            if(output == "" and process.poll() is not None):
                self.update_progressbar(100)
                self.update_speed_label("Download Compelte")
                self.process =None
                break
            if output:
                latest = get_latest_progress(output)
                if latest is not None:
                    self.update_progressbar(latest['progress'])
                    self.update_speed_label(latest['speed'])
                    print(f"Progress: {latest['progress']}%, Speed: {latest['speed']}, ETA: {latest['eta']}")
        if process.returncode != 0:
            print(f"Command failed with error: {process.stderr.read()}")


class queue_download_with_cmd():
    
    def __init__(self):
        self.q_runables = []
        self.q_download_frames = []
        self.old_runables = []
        self.old_download_frames = []
        self.q = queue.Queue()
        self.isdownloading = False
        self.runable = None

    def put(self, run_able_objeckt: downlodad_with_cmd):
        self.q.put(run_able_objeckt)
        
    def abort_curent_prozess(self):
        if  self.runable is not None:
            assert isinstance(self.runable, downlodad_with_cmd), "Queue item is not a valid instance"
            self.runable.abort_process()
    
    def append(self,runable:downlodad_with_cmd,frame:tk.Frame):
        self.q_runables.append(runable)
        self.q_download_frames.append(frame)

    def abort_or_remove(self,runable):
        if runable == self.runable:
            self.abort_curent_prozess()
            self.old_runables.remove(runable)
            dowload_frame = self.old_download_frames.pop(0)
            dowload_frame.destroy()
        else:
            self.remove(runable)

    def remove(self, run_able_objeckt):
        
        temp_list = []
        removed_item = None
        # Dequeue all items, filtering out the one to remove
        while not self.q.empty():
            item = self.q.get()
            if item != run_able_objeckt:
                temp_list.append(item)
            else: 
                removed_item = item
                
        # Re-enqueue the remaining items
        for item in temp_list:
            self.q.put(item)
        if removed_item is not  None:
            i=self.q_runables.index(removed_item)
            dowload_frame = self.q_download_frames.pop(i)
            dowload_frame.destroy()
            self.q_runables.remove(removed_item)
        else:
            i = self.old_runables.index(run_able_objeckt)
            self.old_runables.remove(run_able_objeckt)
            dowload_frame = self.old_download_frames.pop(i)
            dowload_frame.destroy()
   
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
                        self.old_runables.append(self.q_runables.pop(0))
                        self.old_download_frames.append(self.q_download_frames.pop(0))
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
   

   
   
    