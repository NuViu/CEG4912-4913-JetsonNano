
# import sys
# sys.path.insert(1, 'detect_camera_machine.py')

# from module.animal_def import *
from detect_camera_machine import Object_detection
from detect_text_machine import Text_detection
# from CEG4912-4913-JetsonNano/object_detection-model/detect_camera_machine.py
class State_machine:
    def run_machine(self):
       Object_detection.run_object(self)
       Text_detection.run_live(self)
       
if __name__=="__main__":
    x=State_machine()
    x.run_machine()