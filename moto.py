from collections import defaultdict
from datetime import datetime
import cv2
import numpy as np
import math
import time

from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('best.pt')

# Open the video file
video_path = 'C:\\Users\\Júlia\\OneDrive\\Documentos\\code\\pdi\\video2.mp4'
cap = cv2.VideoCapture(video_path)

# Store the frame history
frame_classes = []

if cap.isOpened() == False:
    raise Exception('Não foi possível abrir captura')

frame_count = 0
# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model(frame)
        annotated_frame = results[0].plot()
        classes = results[0].boxes.cls.cpu().tolist()
        names = results[0].names

        for clas in classes:
            frame_classes.append(clas)
        # print(frame_classes)
                            
        # Display the annotated frame
        cv2.imshow("YOLOv8 Tracking", annotated_frame)
        
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()