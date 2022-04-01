from imageai.Detection import VideoObjectDetection
import os
import cv2
import csv

execution_path = os.getcwd()


camera = cv2.VideoCapture(0)

detector = VideoObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath(os.path.join(execution_path , "resnet50_coco_best_v2.1.0.h5"))
detector.loadModel()

def forFrame(frame_number, output_array, output_count):
    print("FOR FRAME ", frame_number)
    keys = output_array[0].keys()

    with open("data_cam.csv", "w", newline="") as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(output_array)

    # print("Output for each object : ",output_array)
    print("Output count for unique objects : ", output_count)
    print("------------END OF A FRAME --------------")

video_path = detector.detectObjectsFromVideo(
                camera_input=camera,
                output_file_path=os.path.join(execution_path, "camera_detected_video"),
                frames_per_second=20,  per_frame_function=forFrame,log_progress=True, minimum_percentage_probability=40,detection_timeout=1)


print(video_path)