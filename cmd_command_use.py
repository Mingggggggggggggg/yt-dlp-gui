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
 
class downlodad_with_cmd():
    
    def __init__(self,json_settings:dict):
        command_parts = []
        command_parts.append(".\\yt-dlp.exe")
        command_parts.append(json_settings["youtube_url"])
        command_parts.append(" ".join([command_args["Re-encode"], json_settings["file_formate"]])) 
        
        
        for arg in list(json_settings):
            if arg in list(command_args):
                command_parts.append(command_args[arg])
        
        self.command = " ".join(command_parts)
        pass
    

    def run (self):
        process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        while True:
            output = process.stdout.readline()
            if(output == "" and process.poll() is not None):
                break
            if output:
                latest = get_latest_progress(output)
                if latest is not None:
                    print(f"Progress: {latest['progress']}%, Speed: {latest['speed']}, ETA: {latest['eta']}")


                




class queue_download_with_cmd():
    
    def __init__(self):
        self.q = queue.Queue()
        self.isdownloading = False

    def put(self, run_able_objeckt: downlodad_with_cmd):
        self.q.put(run_able_objeckt)
    
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
    download_manager.start_download_able()
    download_manager.put(befehl)
    download_manager.put(befehl2)
    download_manager.put(befehl3)
    time.sleep(200)
   

   
   
    