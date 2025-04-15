import sys
import time
import os
import logging
import cv2
import threading
from server.threading_wrapper import Thread
from flask import Blueprint, render_template, Response, request
from server.microscope_camera_control import camera_control_1

from server.settings import Config
from server.extensions import socketio

blueprint = Blueprint("camera_1", __name__, url_prefix="/", static_folder="../static")
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

@blueprint.route("/camera_1", methods=['GET'])
def index():
    return render_template(
        "camera_1.html",
        hostname=Config.HOSTNAME,
    )

@blueprint.route("/camera_1/video_feed")
def video_feed():
    return Response(camera_control_1.yield_frame(), mimetype="multipart/x-mixed-replace; boundary=frame")   

@socketio.on("start-timelapse", namespace="/camera_1")
def timelapse1(message):
    timelapse_name = message["timelapse-name-1"]
    print(timelapse_name)
    if not os.path.isdir(f"Timelapses/{timelapse_name}"):
        os.mkdir(f"Timelapses/{timelapse_name}")
    camera_control_1.timelapse_on = not camera_control_1.timelapse_on
    print(camera_control_1.timelapse_on)
    if (camera_control_1.timelapse_on == True):
        camera_control_1.timelapse_name = timelapse_name
        camera_control_1.start_timelapse()
        print("timelapse started")
    else:
        camera_control_1.stop_timelapse()
        print("timelapse stopped")
    #   camera_1.release()
    #   time.sleep(3)
    #   camera_1 = cv2.VideoCapture(0)
    # 
    
def shutdown(is_critical=False):
    pass