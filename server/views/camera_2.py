import sys
import time
import os
import logging
import cv2
import threading
from server.threading_wrapper import Thread
from flask import Blueprint, render_template, Response, request
from server.microscope_camera_control import camera_control_2

from server.settings import Config
from server.extensions import socketio

blueprint = Blueprint("camera_2", __name__, url_prefix="/", static_folder="../static")
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

@blueprint.route("/camera_2", methods=['GET'])
def index():
    return render_template(
        "camera_2.html",
        hostname=Config.HOSTNAME,
    )

@blueprint.route("/camera_2/video_feed")
def video_feed():
    return Response(camera_control_2.yield_frame(), mimetype="multipart/x-mixed-replace; boundary=frame")   

@socketio.on("initialize-buttons", namespace="/camera_2")
def initialize_buttons ():
    print(f"Emitting camera_states {camera_control_2.camera_is_on}, {camera_control_2.timelapse_on}")
    socketio.emit("camera_states", [camera_control_2.camera_is_on, camera_control_2.timelapse_on], namespace="/camera_2")


@socketio.on("turn-on-camera", namespace="/camera_2")
def turn_on_camera():
    if (camera_control_2.camera_is_on == False):
        camera_control_2.turn_camera_on()
        camera_control_2.camera_is_on = True
        print("turned on camera 2")
        camera_control_2.create_and_start_thread()
        socketio.emit("disable-on-button", namespace="/camera_2")

@socketio.on("turn-off-camera", namespace="/camera_2")
def turn_off_camera():
    if (camera_control_2.camera_is_on == True):
        camera_control_2.camera_is_on = False
        camera_control_2.turn_camera_off()
        print("turned off camera 2")
        socketio.emit("disable-off-button", namespace="/camera_2")

@socketio.on("start-timelapse", namespace="/camera_2")
def start_timelapse(message):
    if (camera_control_2.timelapse_on == False):
        camera_control_2.time_timelapse_started = time.time()
        camera_control_2.timelapse_on = True
        print(camera_control_2.timelapse_on)
        timelapse_name = message["timelapse-name-1"]
        print(timelapse_name)

        if not os.path.isdir(f"Timelapses/{timelapse_name}"):
            os.mkdir(f"Timelapses/{timelapse_name}")
            
        camera_control_2.timelapse_name = timelapse_name

        if (message["timelapse-duration"].isdigit()):
            timelapse_duration = int(message["timelapse-duration"])
            timelapse_duration = timelapse_duration * 60 * 60
            camera_control_2.timelapse_duration = timelapse_duration

        if (message["timelapse-frequency"].isdigit()):
            camera_control_2.timelapse_frequency = int(message["timelapse-frequency"])

        camera_control_2.start_timelapse()
        socketio.emit("disable-timelapse-on-btn", namespace="/camera_2")
        print("timelapse started")

@socketio.on("stop-timelapse", namespace="/camera_2")
def stop_timelapse():
    if (camera_control_2.timelapse_on == True):
        camera_control_2.timelapse_on = False
        camera_control_2.stop_timelapse()
        socketio.emit("disable-timelapse-off-btn", namespace="/camera_2")
        print("timelapse stopped")
    
def shutdown(is_critical=False):
    pass