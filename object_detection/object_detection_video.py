# Based on AIComputerVision https://github.com/mailrocketsystems/AIComputerVision

import cv2
import datetime
import imutils
import numpy as np

PROTOPATH = "MobileNetSSD_deploy.prototxt"
MODELPATH = "MobileNetSSD_deploy.caffemodel"
DETECTOR = cv2.dnn.readNetFromCaffe(prototxt=PROTOPATH, caffeModel=MODELPATH)
# Only enable it if you are using OpenVino environment (pip install openvino)
#DETECTOR.setPreferableBackend(cv2.dnn.DNN_BACKEND_INFERENCE_ENGINE)
#DETECTOR.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]

def frame_2_msec(fps,frame):
    msec = (frame / fps)* 1000
    return msec

def msec_2_smpte(msec):
    sec = msec / 1000
    hours = int((sec // 60 ) // 60)
    minutes = int((sec // 60 ) % 60)
    seconds = int(sec % 60)
    millis = msec % 1000
    smpte = str(hours).zfill(2) + ":" + str(minutes).zfill(2) + ":" + str(seconds).zfill(2) + "." + str(int(millis)).zfill(3)
    return smpte

def main():
    VIDEOPATH = "test-video.mp4"
    DETECTION_TARGET = "car"

    cap = cv2.VideoCapture(VIDEOPATH)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    videofps = float(cap.get(cv2.CAP_PROP_FPS))
    fps_start_time = datetime.datetime.now()
    fps = 0
    current_frame = 0
    detection_start_frame = 0
    detection_end_frame = 0
    target_detected = False
    previous_frame_target_detected = False

    while True:
        ret, frame = cap.read()
        frame = imutils.resize(frame, width=600)
        current_frame = current_frame + 1
        if current_frame >= total_frames:
            print("End of video reached. We're done.")
            break

        (H, W) = frame.shape[:2]

        blob = cv2.dnn.blobFromImage(frame, 0.007843, (W, H), 127.5)

        DETECTOR.setInput(blob)
        object_detections = DETECTOR.forward()

        target_detected = False

        for i in np.arange(0, object_detections.shape[2]):
            confidence = object_detections[0, 0, i, 2]
            if confidence > 0.5:
                idx = int(object_detections[0, 0, i, 1])

                if CLASSES[idx] != DETECTION_TARGET:
                    continue

                object_box = object_detections[0, 0, i, 3:7] * np.array([W, H, W, H])
                (startX, startY, endX, endY) = object_box.astype("int")

                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 1)

                target_detected = True


        fps_end_time = datetime.datetime.now()
        time_diff = fps_end_time - fps_start_time
        if time_diff.seconds == 0:
            fps = 0.0
        else:
            fps = (current_frame / time_diff.seconds)

        current_frame_text = "Frame: " + str(current_frame) + " of " + str(total_frames)
        cv2.putText(frame, current_frame_text, (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)

        fps_text = "FPS: {:.2f}".format(fps) + " of " + str(videofps) 
        cv2.putText(frame, fps_text, (5, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 1)
        
        smpte_text = "SMPTE: " + str(msec_2_smpte(frame_2_msec(videofps,current_frame))) 
        cv2.putText(frame, smpte_text, (5, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 1)

        if previous_frame_target_detected and not target_detected: #Case: Target lost, detection ended.
            #print("no more detection on frame " + str(current_frame))
            detection_end_frame = current_frame - 1
            if detection_start_frame != detection_end_frame:
                #print(DETECTION_TARGET.capitalize() + " detected in sequence from " + str(msec_2_smpte(frame_2_msec(videofps,detection_start_frame))) + " to " + str(msec_2_smpte(frame_2_msec(videofps,detection_end_frame))))
                print("<entry producer=\"chain1\" in=\""+ str(msec_2_smpte(frame_2_msec(videofps,detection_start_frame))) + "\" out=\"" + str(msec_2_smpte(frame_2_msec(videofps,detection_end_frame))) + "\" />" )
            
        if target_detected and not previous_frame_target_detected:
            #print("new detection on frame " + str(current_frame))
            detection_start_frame = current_frame

        if target_detected:
            detection_status_text = DETECTION_TARGET.capitalize() + " detected "
            cv2.putText(frame, detection_status_text, (5, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1)

        previous_frame_target_detected = target_detected

        cv2.imshow("Application", frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            print("Quit command received. Aborted.")
            break

    cv2.destroyAllWindows()


main()
