import numpy as np
import argparse
import imutils
import cv2
import csv
import pytesseract
from imutils.video import VideoStream
from imutils.video import FileVideoStream
from imutils.video import FPS
from imutils.object_detection import non_max_suppression
import time
import threading
import queue
import re
import vlc
from gtts import gTTS  
# from playsound import playsound 

 
class Text_detection:
    running=False
    def prediction_text(self,scores, geometry):

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

                endX = int(offsetX + (cos * data_x1[x]) + (sin * data_x1[x]))
                endY = int(offsetY - (sin * data_x1[x]) + (cos * data_x2[x]))
                startX = int(endX - w)
                startY = int(endY - h)

                rectangles.append((startX, startY, endX, endY))
                confidences.append(data_score[x])
        return (rectangles, confidences)

    def filterFrame(frame):
        frame = imutils.resize(frame, width=450)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = np.dstack([frame, frame, frame])
        return frame

    def video_argument(self):
        x = argparse.ArgumentParser()
        x.add_argument("-v", type=str)
        args = vars(x.parse_args())
        return args
    

        
    def run_live(self):
        # x=Text_detection();
        self.running = True
        args = self.video_argument()
        iters = 0
        time_labels = ['t_capture','t_infer', 't_box','t_show'] #[0.0009343624114990234, 1.134493112564087, 0.0008838176727294922, 0.0002529621124267578]
        avg_times = [0]*len(time_labels)
        times = []
        result = []
        q = queue.Queue()
        results = []
        text_results = []

        W, H = None, None
        new_widths = 640
        new_heights = 640
        ratio_widths, ratio_heights = None, None

        layer_names = ["feature_fusion/Conv_7/Sigmoid", "feature_fusion/concat_3"]

        print("Running text detection model")
       
        net = cv2.dnn.readNet("../text-detection-model/frozen_east_text_detection.pb")

        if not args.get("v", False):
            print("starting live video")
            video_stream = VideoStream(src=0).start()
            time.sleep(1)

        else:
            video_stream = cv2.VideoCapture(args["v"])

        fps = FPS().start()
        tic = time.time()
        while self.running:
            videoframe = video_stream.read()
            videoframe = videoframe[True] if args.get("v", False) else videoframe

            if videoframe is None:
                break

            videoframe = imutils.resize(videoframe, width=320, height=320)
            orig = videoframe.copy()
            orig_height, orig_width = orig.shape[:2]

            if W is None or H is None:
                H, W = videoframe.shape[:2]
                ratio_widths = W / float(new_widths)
                ratio_heights = H / float(new_heights)
            
            videoframe = cv2.resize(videoframe, (new_widths, new_heights))
            rgb = cv2.cvtColor(videoframe, cv2.COLOR_BGR2RGB)
            rgb = imutils.resize(videoframe, width=750)
            blob = cv2.dnn.blobFromImage(
                cv2.resize(rgb,(300, 300)),# 1.0, (104.0, 177.0, 123.0),
                1.0,
                (new_widths, new_heights),
                (104.0, 177.0, 123.0),
                # (123.68, 116.78, 103.94),
                # swapRB=True,
                crop=False,
            )
            net.setInput(blob)
            scores, geometry = net.forward(layer_names)

            rectangles, confidences = self.prediction_text(scores, geometry)
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

                config = "-l eng --oem 1 --psm 8"
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
            res,flag=self.getstring(text_results)
            r=','.join(res)
            if flag==True:
                string_recv="Possible words detected: "+r
                print(string_recv)
                language = 'en'  
                obj = gTTS(text=string_recv,lang=language, slow=False)
                obj.save("audio_text.mp3")
                t1=threading.Thread(target=self.play_sound,args=("audio_text.mp3", ))
                        # self.play_sound("audio_text.mp3")
                t1.start()
            flag=False
            text_results=[]
                        #t1.join()

            toc = time.time()
            fps.update()
            # cv2.imshow("", orig)
           
            key = cv2.waitKey(1)
            # diff=toc-tic

            # if key == ord("q"):
            #     break
            # if diff >= 90:
            #     print(diff)
            #     break
            

        fps.stop()
        print(f"Video runtime : {round(fps.elapsed(), 4)}")
        print(f"Video FPS : {round(fps.fps(), 4)}")
        if not args.get("v", False):
            video_stream.stop()
            video_stream.release.release()
        else:
            video_stream.release()

        cv2.destroyAllWindows()
        
        return (text_results,results)
        
    
    
    def run_video(self,args="v"):
        x=Text_detection(); 
        # args =x.video_argument()
        # args = "-v x.mov"
        # args =x.video_argument()
        results = []
        text_results = []

        W, H = None, None
        new_widths = 640
        new_heights = 640
        ratio_widths, ratio_heights = None, None

        layer_names = ["feature_fusion/Conv_7/Sigmoid", "feature_fusion/concat_3"]

        print("Running text detection model")
        net = cv2.dnn.readNet("../text-detection-model/frozen_east_text_detection.pb")

        if not args!="v":
            print("starting video stream...")
            video_stream = VideoStream(src=0).start()
            time.sleep(1)

        else:
            video_stream = cv2.VideoCapture("x.mov")

        fps = FPS().start()

        while True:

            videoframe = video_stream.read()
            videoframe =videoframe

            if videoframe is None:
                break

            videoframe = imutils.resize(videoframe, width=640)
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

            rectangles, confidences = x.prediction_text(scores, geometry)
            detect_boxes = non_max_suppression(np.array(rectangles), probs=confidences)

            for (start_x, start_y, end_x, end_y) in detect_boxes:

                start_x = int(start_x * ratio_widths)
                start_y = int(start_y * ratio_heights)
                end_x = int(end_x * ratio_widths)
                end_y = int(end_y * ratio_heights)

                delta_x = int((end_x - start_x) *0.25) 
                delta_y = int((end_y - start_y) * 0.25)

                box_region = orig[
                    max(0, start_y-delta_y) : min(orig_height, end_y+(delta_y*2)),
                    max(0, start_x-delta_x) : min(orig_width, end_x+(delta_x*2)),
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
        if not args!="v":
            video_stream.stop()

        else:
            video_stream.release()

        cv2.destroyAllWindows()
        
        return (text_results,results)



    def getstring(self,text_results):  
        giv_list=['Rideau','Nicholas','Arrowroot','Ottawa','Brentford','Toronto','Somerset','Wellington','Bank','Montreal','Elgin','Preston','Bronson'] #given list street names
        u=""
        v=[]
        y=[]
        res=""
        flag=False   
        for i in range(len(text_results)):
            u=text_results[i].lower()+" "
            v.append(re.sub(r'[^A-Za-z0-9 ]+','',u).lower())
        
        for i in v:
            for j in giv_list:
                if i.lower().strip()==j.lower().strip():
                    flag=True
                    y.append(j.lower().strip())
                    
        
        z=set(y)
        res = ', '.join(z)
        #print(v)
        # print("Y str: ",y)
        # print("Z str: ",z)
        # print("Res str: ",res)
        return (z,flag)


        # store in csv
    def store_data_live(self):
        # x=Text_detection(); 
        text_results,results=self.run_live()
        # results = sorted(results, key=lambda r: r[0][1])
        # with open("data.csv", "w", newline="") as output_file:
        #     dict_writer = csv.writer(output_file)
        #     dict_writer.writerows(results)

        # with open("text_data.csv", "w", newline="") as output_file:
        #     dict_writer = csv.writer(output_file)
        #     dict_writer.writerows(text_results)
        
        #print(text_results)
        
        return text_results    
    
    def store_data_video(self,):
        x=Text_detection(); 
        text_results,results=x.run_video(args="v")
        results = sorted(results, key=lambda r: r[0][1])
        with open("data.csv", "w", newline="") as output_file:
            dict_writer = csv.writer(output_file)
            dict_writer.writerows(results)

        with open("text_data.csv", "w", newline="") as output_file:
            dict_writer = csv.writer(output_file)
            dict_writer.writerows(text_results)
        
        print(text_results)
        
        return text_results    
    
    def play_sound(self,filename):
        filename="audio_text.mp3"
        #  playsound(filename)
        p = vlc.MediaPlayer("/home/nuviu/Desktop/Code/audio_text.mp3")
        value = p.get_length()
        if(value < 0):
            value=5
        p.play()
        time.sleep(value)
        p.stop()

    def set_running(self,val):
        self.running=val
        
#if __name__=="__main__":
#    x=Text_detection()
#    T2=threading.Thread(target=x.store_data_live)
#    T2.start()
#    time.sleep(30)
#    T3=threading.Thread(target=x.set_running,args=(False, ))
#    T3.start()
#    T2.join()
#    T3.join()
