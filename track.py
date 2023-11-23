from ultralytics import YOLO

# Load an official or custom model
# model = YOLO('yolov8n.pt')  # Load an official Detect model
# model = YOLO('yolov8n-pose.pt')  # Load an official Pose model
# model = YOLO('path/to/best.pt')  # Load a custom trained model
model = YOLO('yolov8n.pt')  # Load an official Segment model

# Perform tracking with the model
results = model.track(source=0, show=True,save=True)  # Tracking with default tracker
# results = model.track(source="https://youtu.be/LNwODJXcvt4", show=True, tracker="bytetrack.yaml")  # Tracking with ByteTrack tracker