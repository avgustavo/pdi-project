from collections import defaultdict
from datetime import datetime
import cv2
import numpy as np
import math
import time

from ultralytics import YOLO
def estimatespeed(Location1, Location2):
    #Euclidean Distance Formula
    d_pixel = math.sqrt(math.pow(Location2[0] - Location1[0], 2) + math.pow(Location2[1] - Location1[1], 2))
    # defining thr pixels per meter
    # print(Location1[1]/680)
    ppm = 6 + 6 / math.sqrt(math.pow(Location1[1]/680, 2))
    d_meters = d_pixel/(ppm)
    time_constant = 15*3.6
    #distance = speed/time
    speed = d_meters * time_constant

    return int(speed)
# Load the YOLOv8 model
model = YOLO('yolov8n.pt')

# Open the video file
video_path = 'C:\\Users\\Júlia\\OneDrive\\Documentos\\code\\pdi\\v1.mp4'
cap = cv2.VideoCapture(video_path)

# Store the track history
track_history = defaultdict(lambda: [])
speed_history = defaultdict(lambda: [])
start_time = defaultdict(lambda: [])
end_time = defaultdict(lambda: [])
classes_history = defaultdict(lambda: [])

if cap.isOpened() == False:
    raise Exception('Não foi possível abrir captura')

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True)

        a = len(results[0])
        if a !=0:
            # Get the boxes and track IDs
            boxes = results[0].boxes.xywh.cpu()
            track_ids = results[0].boxes.id.int().cpu().tolist()

            # Get Classes, names and confidences
            classes = results[0].boxes.cls.cpu().tolist()
            names = results[0].names

            # Visualize the results on the frame
            annotated_frame = results[0].plot()

            # Plot the tracks
            for box, track_id, clas in zip(boxes, track_ids, classes):
                x, y, w, h = box
                track = track_history[track_id]
                track.append((float(x), float(y)))  # x, y center point
                
                speed = speed_history[track_id]
                
                tipo = classes_history[track_id]
                if len(tipo)== 0:
                    tipo.append(names[clas])

                st = start_time[track_id]
                if len(st)==0:
                    st.append(datetime.now())
                end_time[track_id] = datetime.now()
            

                points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
                teste = np.hstack(track).astype(np.int32)
                    #time.sleep(2)
                
                if(len(teste)>=4):
                    obj_speed =   estimatespeed([teste[len(teste)-4], teste[len(teste)-3]], [teste[len(teste)-2], teste[len(teste)-1]])
                    speed.append(obj_speed)
                    
                    # Defina as configurações do texto
                    fonte = cv2.FONT_HERSHEY_SIMPLEX
                    tamanho_fonte = 1
                    cor = (255, 255, 255)  # Cor do texto em BGR (branco neste exemplo)
                    espessura = 2

                    # Posição do texto no fram
                    texto = str(np.around(np.mean(speed), 1))+' Km/h'

                    # Adicione o texto ao frame
                    cv2.putText(annotated_frame, texto, (teste[len(teste)-2]+8, teste[len(teste)-1]+28), fonte, tamanho_fonte, cor, espessura)

                

                cv2.polylines(annotated_frame, [points], isClosed=False, color=(230, 230, 230), thickness=10)

            # Display the annotated frame
            cv2.imshow("YOLOv8 Tracking", annotated_frame)
            
            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                # print('START')
                # print(start_time)
                # print('END')
                # print(end_time)
                break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()