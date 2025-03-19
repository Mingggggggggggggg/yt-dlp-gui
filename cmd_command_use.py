import queue
import subprocess
import threading
import time


class downlodad_with_cmd():
        
    def __init__(self,json_settings:dict):
        self.command = "Hallo"
        pass
    
    

    def run (self):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)




class queue_download_with_cmd():
    
    def __init__(self):
        self.q = queue.Queue()

    def start_download_able(self):
        def run_if_able():
            while True:
                if not self.q.empty():
                    while not self.q.empty():
                        runable = self.q.get()
                        assert isinstance(runable, downlodad_with_cmd), "Queue item is not a valid instance"

                        runable.run()
                print("Hallo")
                time.sleep(1)
        
        thread = threading.Thread(target=run_if_able, daemon=True)
        thread.start() 
    
    def put(self, run_able_objeckt: downlodad_with_cmd):
        self.q.put(run_able_objeckt)

if __name__ == "__main__":
    download = queue_download_with_cmd()
    download.start_download_able()
    time.sleep(10)