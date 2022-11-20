import argparse
from typing import Dict
from typing_extensions import Self
from gtts import gTTS  
from playsound import playsound  
from detect_text import Text_detection

# from enchant import DictWithPWL
# from enchant.checker import SpellChecker


x=Text_detection()
text_results=x.store_data_live()

def getstring():
    u=""
    # for i in range(len(text_results)):
    #    s={};
    #    x=text_results[i]+""
    #    my_dict = Dict("en_US")
    #    my_checker = my_dict.check(x)
    #    if my_checker==True:
    #        s.add(my_dict)
       
        
    for i in range(len(text_results)):
       u+=text_results[i]+" "
       
    return u

print(getstring())  
# my_dict = DictWithPWL("en_US", getstring())
# my_checker = SpellChecker(my_dict)
language = 'en'  
obj = gTTS(text=getstring(),lang=language, slow=False)


# obj.save("test.mp3")  
  
# playsound("test.mp3") 
