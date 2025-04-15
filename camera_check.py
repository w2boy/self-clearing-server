import cv2, glob

for camera in glob.glob("/dev/video*"):
    cap = cv2.VideoCapture(camera)
    if cap.isOpened():
        print(f"Camera found at: {camera}")
        # Do something with the camera
        cap.release()