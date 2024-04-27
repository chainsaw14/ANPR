from ultralytics import YOLO
import cv2
import numpy as np
from sort.sort import *
from util import get_car, read_license_plate, write_csv
from datetime import datetime
from database import store
import os
file_path = './/data//test.csv'
if os.path.exists(file_path):
    os.remove(file_path)
current_datetime = datetime.now()
time = current_datetime.strftime("%d-%m-%Y %H:%M:%S")
results = {}
mot_tracker = Sort()
# load models
coco_model = YOLO('yolov8n.pt')
license_plate_detector = YOLO('./model/license_plate_detector.pt')
# load video

vehicles = [2, 3, 5, 7]
def detection(cap):
    # read frames
    # It takes argument as a cv2 image object or a cv2 video object
    cap = cv2.VideoCapture("C:\\Users\\Harsh\\Downloads\\small multi.mp4")
    frame_nmr = -1
    ret = True
    while ret:
        frame_nmr += 1
        ret, frame = cap.read()
        if ret:
            results[frame_nmr] = {}
            print("detect cehicle")
            # detect vehicles
            detections = coco_model(frame)[0]
            detections_ = []
            for detection in detections.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = detection
                if int(class_id) in vehicles:
                    detections_.append([x1, y1, x2, y2, score])

            # track vehicles
            print("track vehicle")
            track_ids = mot_tracker.update(np.asarray(detections_))

            # detect license plates
            print("detect license plate")
            license_plates = license_plate_detector(frame)[0]
            for license_plate in license_plates.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = license_plate

                # assign license plate to car
                print("assigning")
                xcar1, ycar1, xcar2, ycar2, car_id = get_car(license_plate, track_ids)

                if car_id != -1:

                    # crop license plate
                    license_plate_crop = frame[int(y1):int(y2), int(x1): int(x2), :]

                    # process license plate
                    license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
                    _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 0, 255, cv2.THRESH_BINARY_INV)
                    current_datetime = datetime.now()
                    time = current_datetime.strftime("%d-%m-%Y %H-%M-%S") 
                    # read license plate number
                    license_plate_text, license_plate_text_score = read_license_plate(license_plate_crop_gray)
                    print("This is detected licence plate= "+str(license_plate_text))
                    if license_plate_text is not None:
                        results[frame_nmr][car_id] = {'car': {'bbox': [xcar1, ycar1, xcar2, ycar2]},
                                                    'license_plate': {'bbox': [x1, y1, x2, y2],
                                                                        'text': license_plate_text,
                                                                        'bbox_score': score,
                                                                        'text_score': license_plate_text_score},
                                                                        'time': time}

    # write results

    print("Results")
    write_csv(results, './/data//test.csv')
    store()
if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description="ANPR system")

    # Add argument for video path
    parser.add_argument("--video_path", type=str, help="Path to the video file")

    # Parse the arguments
    args = parser.parse_args()

    # Call main function with the provided video path
    detection(args.video_path)
