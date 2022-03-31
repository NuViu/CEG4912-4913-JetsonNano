from imageai.Detection import VideoObjectDetection
import os
import csv

execution_path = os.getcwd()

detector = VideoObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath( os.path.join(execution_path , "resnet50_coco_best_v2.1.0.h5"))
detector.loadModel()

def forFrame(frame_number, output_array, output_count):
    print("FOR FRAME " , frame_number)
    keys = output_array[0].keys()

    with open('data.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(output_array)

    #print("Output for each object : ",output_array)
    print("Output count for unique objects : ", output_count)
    print("------------END OF A FRAME --------------")

#will run for 5 seconds
video_path = detector.detectObjectsFromVideo(input_file_path=os.path.join(execution_path, "traffic.mp4"),
                                output_file_path=os.path.join(execution_path,"traffic_detection")
                                , frames_per_second=20,per_frame_function=forFrame, log_progress=True,detection_timeout=1) 



print(video_path)

import csv


