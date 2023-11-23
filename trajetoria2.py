import cv2
from ultralytics import YOLO
import numpy as np

video_path = 'C:\\Users\\Júlia\\OneDrive\\Documentos\\code\\yt\\V1.mp4'

cap = cv2.VideoCapture(video_path)
all_centroids = []
model = YOLO('yolov8n.pt')  # Load an official Segment model

while True:
    ret, frame = cap.read()
    if not ret:
        break
    results = model(frame)
    for r in results:
        boxes = r.boxes.xyxy # Obtem as bounding boxes no formato xyxy
        for box in boxes:
            x1, y1, x2, y2 = box
            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)
            all_centroids.append((cx, cy))
            # Desenha bounding box e centróide
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0,255,0), 2)
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
    # Desenhe a trajetória
    if len(all_centroids) > 1:
        cv2.polylines(frame, [np.array(all_centroids)], False, (255, 0, 0), 2)
    
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27: # Esc key
        break
cap.release()
cv2.destroyAllWindows()
