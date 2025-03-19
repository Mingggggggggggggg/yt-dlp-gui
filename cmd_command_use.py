import queue
import subprocess
import threading
import time
import re 

#Help Function for use not relevant for class 
command_args = {
        "Re-encode" : "--recode-video",
        "write-thumbnail":"--write-thumbnail",
        "write-all-thumbnails":"--write-all-thumbnails",
        "list-thumbnails":"--list-thumbnails ",
        "keep-video":"-k"
        }

def parse_progress(output):
        match = re.search(r"Progress: (\d+)%", output)
        if match:
            return int(match.group(1))
        return None
 
class downlodad_with_cmd():
    
    def __init__(self,json_settings:dict):
        command_parts = [".\yt-dlp.exe"]
        command_parts.append(json_settings["youtube_url"])
        command_parts.append("".join([command_args["Re-encode"], json_settings["file_formate"]])) 
        for arg in json_settings.keys[1:]:
            if arg in command_args.keys:
                command_parts.append(command_args[arg])
        
        self.command = "".join(command_parts)
        pass
    

    def run (self):
        process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        while True:
            output = process.stdout.readline()
            if(output == "" and process.poll() is not None):
                break
            if output:
                progress = parse_progress(output)
                if progress is not None:
                    print(f"Progress: {progress}%")




class queue_download_with_cmd():
    
    def __init__(self):
        self.q = queue.Queue()
        self.isdownloading = False

    def start_download_able(self):
        def run_if_able():
            while True:
                if not self.q.empty():
                    while not self.q.empty():
                        self.isdownloading = True 
                        runable = self.q.get()
                        assert isinstance(runable, downlodad_with_cmd), "Queue item is not a valid instance"
                        runable.run()
                        self.isdownloading = False
                time.sleep(1)
        
        thread = threading.Thread(target=run_if_able, daemon=True)
        thread.start() 
    
    def put(self, run_able_objeckt: downlodad_with_cmd):
        self.q.put(run_able_objeckt)



if __name__ == "__main__":
    download = queue_download_with_cmd()
    download.start_download_able()
    time.sleep(10)