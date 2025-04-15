import sys
import time
import os
import logging
import cv2
import threading
import glob
from server.threading_wrapper import Thread
from flask import Blueprint, render_template, Response, request

class microscope_camera_control:

    def __init__(self, camera_number):

        self.camera_number = camera_number
        self.camera_driver_index = None
        self.timelapse_on = False
        self.stop_event = threading.Event()
        self.stop_event.set()
        self.timelapse_name = ""
        self.time_timelapse_started = None
        self.timelapse_duration = 86400 # Default: A timelapse will last for 24 Hours
        self.timelapse_frequency = 60 # Default: A picture is taken every 60 seconds
        self.camera = None
        self.camera_is_on = False
        # Use Placeholder image to display at the beginning before the camera is ever turned on
        self.read_frame = cv2.imread('black.png',0)
        self.ret, self.buffer = cv2.imencode('.jpg', self.read_frame)
        self.frame_to_display = self.buffer.tobytes()

        self.timelapse_thread = None

    def create_and_start_thread(self):
        self.timelapse_thread = Thread(log=None, target=self.gen_frames, args=())
        self.timelapse_thread.start()

    def add_frame_number(self, frame, count, font_path="arial.ttf", font_scale=1, font_color=(255, 255, 255), thickness=2):
        # Load the image
        if frame is None:
            print(f"Failed to load image: {image_path}")
            return
        
        # Get image dimensions
        height, width, _ = frame.shape

        # Define the text to be added
        text = f"Frame {count}"

        # Use OpenCV's putText for text rendering
        font = cv2.FONT_HERSHEY_SIMPLEX
        (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)
        x = width - text_width - 10  # 10px padding
        y = height - 10  # 10px padding from bottom

        # Add the text
        cv2.putText(frame, text, (x, y), font, font_scale, font_color, thickness)

        return frame

    # There was a problem where the camera would get a select() timeout error after running the cameras for longer than a day. 
    # This function will reset the cameras at an hourly interval to try and avoid this error.
    def reset_camera(self):
        try:
            self.camera.release()
        except:
            print(f"Tried to release camera {(self.camera_driver_index)} but it failed.")
            print("Perhaps this was caused by the select timeout error or was released previously?")
        self.camera = cv2.VideoCapture(self.camera_driver_index)
        self.camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        print(f"Camera reset at: {self.camera_driver_index}")

    def gen_frames(self):
        time_from_last_frame = 1
        count = 1
        time_camera_started = time.time()
        while(self.camera.isOpened()):
            if (time.time() - time_camera_started > 3600):
                self.reset_camera()
                time_camera_started = time.time()
            success, frame =  self.camera.read()
            if success == True:
                frame = cv2.convertScaleAbs(frame, alpha=1.0, beta=0)
                ret, buffer = cv2.imencode('.jpg', frame)
                # Calculate time passed, if timelapse_frequency has passed save the frame
                current_time = time.time()
                if not self.stop_event.is_set() and ((current_time - self.time_timelapse_started) < self.timelapse_duration):
                    if ((current_time - time_from_last_frame) > self.timelapse_frequency):
                        frame = self.add_frame_number(frame, count)
                        cv2.imwrite(f"Timelapses/{self.timelapse_name}/{self.timelapse_name}_{count}.jpg", frame)
                        count += 1
                        print(f"took a picture! (camera {self.camera_number})")
                        # Reset Timer
                        time_from_last_frame = current_time
                self.frame_to_display = buffer.tobytes()
                # yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")
            else:
                break
        print(f"thread stopped (camera {self.camera_number})")

    def yield_frame(self):
        while(True):
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + self.frame_to_display + b"\r\n")

    def start_timelapse(self):
        self.stop_event.clear()

    def stop_timelapse(self):
        self.stop_event.set()

    def turn_camera_on(self):
        for microscope_camera in glob.glob("/dev/video*"):
            if cv2.VideoCapture(microscope_camera).isOpened():
                video_number = int(microscope_camera.replace("/dev/video", ""))
                if video_number < 10:
                    self.camera_driver_index = video_number
                    self.camera = cv2.VideoCapture(video_number)
                    self.camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
                    print(f"Camera found at: {microscope_camera}")
                    break
    
    def turn_camera_off(self):
        self.camera.release()

camera_control_1 = microscope_camera_control(1)

camera_control_2 = microscope_camera_control(2)

camera_control_3 = microscope_camera_control(3)

camera_control_4 = microscope_camera_control(4)


