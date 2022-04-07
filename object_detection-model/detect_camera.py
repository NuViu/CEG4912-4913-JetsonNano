from imageai.Detection import VideoObjectDetection
import os
import cv2
import csv

execution_path = os.getcwd()


camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH,256);
camera.set(cv2.CAP_PROP_FRAME_HEIGHT,256);

detector = VideoObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath(os.path.join(execution_path , "./object_detection-model/resnet50_coco_best_v2.1.0.h5"))
detector.loadModel()

# def forFrame(frame_number, output_array, output_count):
    # print("FOR FRAME ", frame_number)
    # keys = output_array[0].keys()

    # with open("data_cam.csv", "w", newline="") as output_file:
    #     dict_writer = csv.DictWriter(output_file, keys)
    #     dict_writer.writeheader()
    #     dict_writer.writerows(output_array)

    # # print("Output for each object : ",output_array)
    # print("Output count for unique objects : ", output_count)
    # print("------------END OF A FRAME --------------")

video_path = detector.detectObjectsFromVideo(
                camera_input=camera,
                output_file_path=os.path.join(execution_path, "./object_detection-model/output_video/camera_detect_test"),
                frames_per_second=20, log_progress=True, minimum_percentage_probability=40,detection_timeout=1)


print(video_path)