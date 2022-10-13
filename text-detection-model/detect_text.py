import numpy as np
import argparse
import imutils
import time
import cv2
import csv
import pytesseract
from imutils.video import VideoStream
from imutils.video import FPS
from imutils.object_detection import non_max_suppression
from distutils.command.config import config


def prediction_text(scores, geometry):

    (numrows, numcols) = scores.shape[2:4]
    rectangles = []
    confidences = []

    for y in range(0, numrows):

        data_score = scores[0, 0, y, :]
        data_x0 = geometry[0, 0, y, :]
        data_x1 = geometry[0, 1, y, :]
        data_x2 = geometry[0, 2, y, :]
        data_x3 = geometry[0, 3, y, :]
        data_angle = geometry[0, 4, y, :]

        for x in range(0, numcols):

            if data_score[x] < 0.5:
                continue

            (offsetX, offsetY) = (x * 4.0, y * 4.0)

            angle = data_angle[x]
            cos = np.cos(angle)
            sin = np.sin(angle)

            h = data_x0[x] + data_x2[x]
            w = data_x1[x] + data_x3[x]

            endX = int(offsetX + (cos * data_x1[x]) + (sin * data_x2[x]))
            endY = int(offsetY - (sin * data_x1[x]) + (cos * data_x2[x]))
            startX = int(endX - w)
            startY = int(endY - h)

            rectangles.append((startX, startY, endX, endY))
            confidences.append(data_score[x])
    return (rectangles, confidences)


def video_argument():
    x = argparse.ArgumentParser()
    x.add_argument("-v", type=str)
    args = vars(x.parse_args())
    return args


if __name__ == "__main__":

    args = video_argument()
    results = []
    text_results = []

    W, H = None, None
    new_widths = 640
    new_heights = 640
    ratio_widths, ratio_heights = None, None

    layer_names = ["feature_fusion/Conv_7/Sigmoid", "feature_fusion/concat_3"]

    print("Running text detection model")
    net = cv2.dnn.readNet("frozen_east_text_detection.pb")

    if not args.get("v", False):
        print("[INFO] starting video stream...")
        video_stream = cv2.VideoCapture('nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3280, height=2464, format=(string)NV12, framerate=(fraction)20/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink' , cv2.CAP_GSTREAMER)
        #VideoStream(src=0).start()
        time.sleep(1)

    else:
        video_stream = cv2.VideoCapture(args["v"])

    fps = FPS().start()

    while True:

        videoframe = video_stream.read()
        videoframe = videoframe[True] if args.get("v", False) else videoframe

        if videoframe is None:
            break

        videoframe = imutils.resize(videoframe, width=1000, height=1000)
        orig = videoframe.copy()
        orig_height, orig_width = orig.shape[:2]

        if W is None or H is None:
            H, W = videoframe.shape[:2]
            ratio_widths = W / float(new_widths)
            ratio_heights = H / float(new_heights)

        videoframe = cv2.resize(videoframe, (new_widths, new_heights))

        blob = cv2.dnn.blobFromImage(
            videoframe,
            1.0,
            (new_widths, new_heights),
            (123.68, 116.78, 103.94),
            swapRB=True,
            crop=False,
        )
        net.setInput(blob)
        scores, geometry = net.forward(layer_names)

        rectangles, confidences = prediction_text(scores, geometry)
        detect_boxes = non_max_suppression(np.array(rectangles), probs=confidences)

        for (start_x, start_y, end_x, end_y) in detect_boxes:

            start_x = int(start_x * ratio_widths)
            start_y = int(start_y * ratio_heights)
            end_x = int(end_x * ratio_widths)
            end_y = int(end_y * ratio_heights)

            box_region = orig[
                max(0, start_y) : min(orig_height, end_y),
                max(0, start_x) : min(orig_width, end_x),
            ]

            config = "-l eng --oem 1 --psm 7"
            text = pytesseract.image_to_string(box_region, config=config)

            cv2.rectangle(orig, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)
            cv2.putText(
                orig,
                text,
                (start_x, start_y - 10),
                cv2.FONT_HERSHEY_PLAIN,
                1.0,
                (65, 105, 225),
                2,
            )
            results.append(((start_x, start_y, end_x, end_y), text))
            text_results.append(text)

        fps.update()

        cv2.imshow("", orig)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    fps.stop()
    print(f"Video runtime : {round(fps.elapsed(), 4)}")
    print(f"Video FPS : {round(fps.fps(), 4)}")
    if not args.get("video", False):
        video_stream.stop()

    else:
        video_stream.release()

    cv2.destroyAllWindows()

    # store in csv
    results = sorted(results, key=lambda r: r[0][1])
    with open("data.csv", "w", newline="") as output_file:
        dict_writer = csv.writer(output_file)
        dict_writer.writerows(results)

    with open("text_data.csv", "w", newline="") as output_file:
        dict_writer = csv.writer(output_file)
        dict_writer.writerows(text_results)

