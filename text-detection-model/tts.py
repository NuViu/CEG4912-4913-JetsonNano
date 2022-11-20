import argparse
from gtts import gTTS  
from playsound import playsound  
from detect_text_machine import Text_detection
import re
# from enchant import DictWithPWL
# from enchant.checker import SpellChecker


x=Text_detection()
text_results=x.store_data_live()

def getstring():
    u=""
    v=[]
    res=""
        
    for i in range(len(text_results)):
       u+=text_results[i]+" "
       v.append(re.sub(r'[^A-Za-z0-9 ]+','',u))
    # [print(i) for i in v]
    # new_v = list(dict.fromkeys(v))
    # for i in range(len(v)):
    #      res+=v[i]+" "

    return v[-1]

print("Answer:", getstring())  
# my_dict = DictWithPWL("en_US", getstring())
# my_checker = SpellChecker(my_dict)
language = 'en'  
obj = gTTS(text=getstring(),lang=language, slow=False)


obj.save("test.mp3")  
  
# playsound("test.mp3") 


