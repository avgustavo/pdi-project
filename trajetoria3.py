from collections import defaultdict
from datetime import datetime
import cv2
import numpy as np

from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')

# Open the video file
video_path = 'C:\\Users\\Júlia\\OneDrive\\Documentos\\code\\pdi\\video.mp4'
cap = cv2.VideoCapture(video_path)

# Store the track history
track_history = defaultdict(lambda: [])
start_time = defaultdict(lambda: [])
end_time = defaultdict(lambda: [])
iniciado = defaultdict(lambda: [])

if cap.isOpened() == False:
    raise Exception('Não foi possível abrir captura')

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True)

        # Get the boxes and track IDs
        boxes = results[0].boxes.xywh.cpu()
        track_ids = results[0].boxes.id.int().cpu().tolist()

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Plot the tracks
        for box, track_id in zip(boxes, track_ids):
            x, y, w, h = box
            track = track_history[track_id]
            print(f'1{track_id} .. {track}')
            track.append((float(x), float(y)))  # x, y center point
            print(f'2{track_id} .. {track}')
            st = start_time[track_id]
            if len(st)==0:
                st.append(datetime.now())
            end_time[track_id] = datetime.now()

            # if len(track) > 30:  # retain 90 tracks for 90 frames
            #     track.pop(0)

            # Draw the tracking lines
            points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
            cv2.polylines(annotated_frame, [points], isClosed=False, color=(230, 230, 230), thickness=10)

        # Display the annotated frame
        cv2.imshow("YOLOv8 Tracking", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            print('START')
            print(start_time)
            print('END')
            print(end_time)
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()

