
# import sys

from threaded_object_detection_camera import Object_detection
from detect_text_machine_threaded import Text_detection
import threading
import time
import vlc

class State_machine:
    # Dummy Values To Create Variables
    obj=0
    text=0
    T0=0
    TX=0
    T2=0

    def startup(self):
        self.obj=Object_detection()
        self.text=Text_detection()
        T0=threading.Thread(target=self.dummy_thread)
        TX=threading.Thread(target=self.dummy_thread)
        T2=threading.Thread(target=self.dummy_thread)

    def run_object(self):
        # OBJECT DETECTION #
        self.T0=threading.Thread(target=self.obj.run_object)
        self.T0.start()
        time.sleep(20)
        self.TX=threading.Thread(target=self.tts_object)
        self.TX.start()

    def stop_object(self):
            if(self.T0.isAlive()):
                self.obj.setRunning(False)
                self.T0.join()
            if(self.TX.isAlive()):
                self.TX.join()

    def run_text(self):
        # TEXT DETECTION #
        self.T2=threading.Thread(target=self.text.store_data_live)
        self.T2.start()

    def stop_text(self):
        if(self.T2.isAlive()):
            self.text.set_running(False)
            self.T2.join()
    
    def tts_object(self):
        while self.obj.running:
            try:
                p = vlc.MediaPlayer("/home/nuviu/Desktop/Code/audio_object.mp3")        
                value = p.get_length()
                if(value < 0):
                    value=5
                p.play()
                time.sleep(value)
                p.stop()
                time.sleep(10-value)
            except:
                time.sleep(2)

    def dummy_thread(self):
            print("I DO NOTHING")

#if __name__=="__main__":
#    x=State_machine()
#    x.startup()
#    x.run_object()
#    x.run_text()
#    x.run_object()
#    x.run_text()
