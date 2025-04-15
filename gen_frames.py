import sys
import time
import os
import logging
import cv2
import threading
from server.threading_wrapper import Thread
from flask import Blueprint, render_template, Response, request

from server.settings import Config
from server.extensions import socketio

def gen_frames_1(timelapse_name, timelapse_on, camera_1):
    time_from_last_frame = 1
    count = 1
    if (camera_1 == None) or (not camera_1.isOpened):
        camera_1 = cv2.VideoCapture(0)

    # fps = 5
    # if camera_1.set(cv2.CAP_PROP_FPS, fps):
    #     print(f"Successfully set frame rate to {fps} FPS.")
    # else:
    #     print(f"Failed to set frame rate to {fps} FPS.")
    
    print("running script")
    while(camera_1.isOpened()):
        success, frame = camera_1.read()
        if success == True:
            ret, buffer = cv2.imencode('.jpg', frame)
            if (timelapse_on == True):
                # Calculate time passed, if 60 seconds have passed save the frame
                current_time = time.time()
                if ((current_time - time_from_last_frame) > 5):
                    cv2.imwrite(f"Timelapses/{timelapse_name}/{count}.jpg", frame)
                    count += 1
                    print("took a picture!")
                    # Reset Timer
                    time_from_last_frame = current_time
            frame = buffer.tobytes()
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")
        else:
            break