import jetson_inference
import jetson.utils
import time
import threading
import vlc
import math
from gtts import gTTS
from playsound import playsound

class Object_detection:

    screen_w = 640
    screen_h = 480
    net = jetson_inference.detectNet("ssd-mobilenet-v2", threshold=0.5)
    camera = 0;
    display = jetson.utils.glDisplay()
    initial = True
    running = False

    def run_object(self):
        self.openCamera()
        self.running = True
        while self.running:
            img, width, height = self.camera.CaptureRGBA()
            detections = self.net.Detect(img, width, height)
            objects = set()
            for item in detections:
                objects.add(self.net.GetClassDesc(item.ClassID))
                #print(self.net.GetClassDesc(item.ClassID))
            #print(*detections, sep=",")
            #display.RenderOnce(img, width, height)
            #display.SetTitle("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))

            if(self.initial == True):
                self.initial = False
                start_time = time.time()
            end_time = time.time()    
            cur_time=math.floor(end_time - start_time) 
            
            if(cur_time % 10 == 0 and cur_time > 0):
                string_recv="Possible objects detected: "
                for item in objects:
                    string_recv += item + " "
                print(string_recv)
                language = 'en'  
                obj = gTTS(text=string_recv,lang=language, slow=False)
                obj.save("audio_object.mp3")
    
            if(end_time - start_time > 30):
                break

        self.camera.Close()
        self.running = False
        self.initial = True
        return objects

    def setRunning(self, value):
         print(value)
         self.running=value

    def getRunning(self):
        return self.running

    def closeCamera(self):
        self.camera.Close()
    
    def openCamera(self):
        self.camera = jetson.utils.gstCamera(640, 480, "/dev/video0")

    #def play_sound(self):
    #    #playsound("audio_object.mp3")
    #    p = vlc.MediaPlayer("home/nuviu/Desktop/test-object-TRT/audio_object.mp3")        
    #    value = p.get_length()
    #    if(value < 0):
    #        value=5
    #    p.play()
    #    time.sleep(value)
    #    p.stop()

if __name__=="__main__":
    x=Object_detection()
    try:
        print("0")
        t1=threading.Thread( target=x.run_object )
        print ("1")
        t1.start()
        print ("2")
        time.sleep(20)
        print ("3")
        t2=threading.Thread( target=x.play_sound)
        print ("4")
        t2.start()
        print ("5")

        ##############
        t1.join()
        print ("6")

        t2.join()
        print ("7")

    except Exception as e:
        print ("Error: unable to start thread")
        print(e)
