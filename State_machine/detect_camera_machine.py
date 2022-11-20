from imageai.Detection import VideoObjectDetection
import os
import cv2
import csv
import sys
class Object_detection:
    
    execution_path = os.getcwd()


    camera = cv2.VideoCapture(0)

    detector = VideoObjectDetection()
    detector.setModelTypeAsRetinaNet()
    detector.setModelPath(os.path.join(execution_path , "/path /resnet50_coco_best_v2.1.0.h5"))
    detector.loadModel(detection_speed="flash")
    
    def forFrame(self,frame_number, output_array, output_count):
        print("FOR FRAME ", frame_number)
        keys = output_array[0].keys()
        list_objects = ["Person", "Traffic Light"]
        # with open("data_cam.csv", "w", newline="") as output_file:
        #     dict_writer = csv.DictWriter(output_file, keys)
        #     dict_writer.writeheader()
        #     dict_writer.writerows(output_array)

        print("Output for each object : ",output_array)

        print("Output count for unique objects : ", output_count)
        print("Output count for unique objects : ", output_count.values())
        print("Output count for unique objects : ", list(output_count.keys()))
        list_revcived=list(output_count.keys())
        print(type(output_array))
        for i in (list_revcived):
            for j in (list_objects):
                if(i.lower()==j.lower()):
                    print("object same")
                    # sys.exit("Object Ending")
                
            
            
        # print(type(list(output_count.keys())))
        print("------------END OF A FRAME --------------")
    
    
    
    def run_object(self):
        x=Object_detection()
        video_path = x.detector.detectObjectsFromVideo(
                camera_input=x.camera,
                output_file_path=os.path.join(x.execution_path, "/path/output_video/camera_detect"),
                frames_per_second=5,  per_frame_function=x.forFrame,log_progress=True, minimum_percentage_probability=40,detection_timeout=1)

        video_path
        
        
        

# if __name__=="__main__":
#     x=Object_detection()
#     x.run_object()