import argparse
from gtts import gTTS  
# from playsound import playsound  
from detect_text_machine import Text_detection
import re

class TTS:
    
    
    def getstring(self,text_results):  
        giv_list=['Rideau','Nicholas','Arrowroot','Ottawa','Brentford','Toronto'] #given list street names
        u=""
        v=[]
        y=[]
        res=""
            
        for i in range(len(text_results)):
            u=text_results[i].lower()+" "
            v.append(re.sub(r'[^A-Za-z0-9 ]+','',u).lower())
        
        for i in v:
            for j in giv_list:
                if i.lower().strip()==j.lower().strip():
                    # print("true")
                    y.append(j.lower().strip())
                    
        
        z=set(y)
        res = ', '.join(z)
        print(v)
        # print("Y str: ",y)
        # print("Z str: ",z)
        # print("Res str: ",res)
        return res

    def run_TTS(self):
        x=Text_detection()
        y=TTS()
        text_results=x.store_data_live()
        string_recv="Possible words detected by the text ml model are as follows: "+y.getstring(text_results)
        language = 'en'  
        obj = gTTS(text=string_recv,lang=language, slow=False)
        obj.save("audio_text.mp3")
        #playsound("test.mp3")  
        

if __name__=="__main__":
    x=TTS()
    x.run_TTS()