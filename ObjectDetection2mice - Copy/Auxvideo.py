import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
# model = YOLO('J:/TestDeeplearning/ObjectDetection/Yolo/Yolo/runs/detect/yoloSecondTest/weights/best.pt')
model = YOLO('C:/Users/Administrator/runs/detect/yoloNewB2/weights/best.pt')

# Open the video file
video_path = "F:/PoseYolo/train/data/movies/M974.avi"
video_output = "F:/PoseYolo/train/data/movies/M974Yolo2.avi"

cap = cv2.VideoCapture(video_path)
# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

out = cv2.VideoWriter(video_output,cv2.VideoWriter_fourcc('M','J','P','G'), 30, (frame_width,frame_height))

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 inference on the frame
        results = model.predict(frame,conf = 0.1,workers = 0, device = 0)
       # results = model.predict(frame,conf = 0.3)
        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the annotated frame
        #cv2.imshow("YOLOv8 Inference", annotated_frame)
        # Write the frame into the file 'output.avi'
        out.write(annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
out.release()
cv2.destroyAllWindows()
