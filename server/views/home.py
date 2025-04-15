import sys
import logging
import cv2
import threading
from server.threading_wrapper import Thread
from flask import Blueprint, render_template, Response, send_file
import os
import shutil

from server.settings import Config
from server.extensions import socketio


blueprint = Blueprint("home", __name__, url_prefix="/", static_folder="../static")
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


@blueprint.route("/")
def index():
    directory_path = '/home/self-clearing/Self_Clearing_Server/Timelapses'  # Replace with the actual path
    all_items = os.listdir(directory_path)
    directories = [item for item in all_items if os.path.isdir(os.path.join(directory_path, item))]
    return render_template(
        "home.html",
        hostname=Config.HOSTNAME, directories=directories
    )

@socketio.on("prepare-directory", namespace="/home")
def prepare_directory(message):
    timelapse_directory = message["timelapse-directory"]
    timelapse_path = "/home/self-clearing/Self_Clearing_Server/Timelapses"
    
    if os.path.isdir(f"{timelapse_path}/{timelapse_directory}"):
        shutil.make_archive(f"/home/self-clearing/Self_Clearing_Server/{timelapse_directory}", "zip", timelapse_path, timelapse_directory)
        socketio.emit("download-ready", timelapse_directory, namespace="/home")
    else:
        socketio.emit("invalid-directory", namespace="/home")

@blueprint.route("/download/<timelapse_directory>")
def download_timelapse(timelapse_directory):
    timelapse_path = "/home/self-clearing/Self_Clearing_Server/Timelapses"
    zip_path = f"/home/self-clearing/Self_Clearing_Server/{timelapse_directory}.zip"
    # Serve the ZIP file
    return send_file(zip_path, as_attachment=True)

@socketio.on("prepare-video", namespace="/home")
def prepare_video(message):
    timelapse_path = "/home/self-clearing/Self_Clearing_Server/Timelapses"
    timelapse_directory = message["timelapse-directory"]
    output_dir = "/home/self-clearing/Self_Clearing_Server/Timelapse_Videos"
    frames_folder = timelapse_path + "/" + timelapse_directory
    if os.path.isdir(f"{timelapse_path}/{timelapse_directory}"):
        
        output_file = os.path.join(output_dir, timelapse_directory + '.mp4') # .mp4 or .avi
        fps = 60
        frame_width = 640  # Adjust as needed
        frame_height = 480  # Adjust as needed

        codec = cv2.VideoWriter_fourcc(*'mp4v')  # Adjust codec as needed, mp4v or XVID
        out = cv2.VideoWriter(output_file, codec, fps, (frame_width, frame_height))

        processed_count = 0

        for filename in sorted(os.listdir(frames_folder), key=lambda f: int(''.join(filter(str.isdigit, f)))):

            if filename.endswith('.jpg'):
                img_path = os.path.join(frames_folder, filename)
                frame = cv2.imread(img_path)
                if frame is not None:
                    frame = cv2.resize(frame, (frame_width, frame_height))
                    out.write(frame)
                    processed_count += 1
                    print("Working! Number of Images Processed: ", processed_count)

        out.release()
        print(f"Timelapse video saved as {output_file}.")

        socketio.emit("video-download-ready", timelapse_directory, namespace="/home")
    else:
        socketio.emit("invalid-directory", namespace="/home")

@blueprint.route("/download_video/<timelapse_directory>")
def download_video(timelapse_directory):
    timelapse_path = "/home/self-clearing/Self_Clearing_Server/Timelapse_Videos"
    video_path = f"/home/self-clearing/Self_Clearing_Server/Timelapse_Videos/{timelapse_directory}.mp4"
    # Serve the mp4 file
    return send_file(video_path, as_attachment=True)

@socketio.on("delete-directory", namespace="/home")
def prepare_video(message):
    timelapse_directory = message["timelapse-directory"]
    directory_path = "/home/self-clearing/Self_Clearing_Server/Timelapses/" + timelapse_directory
    if os.path.isdir(directory_path):
        shutil.rmtree(directory_path)
        zip_path = f"/home/self-clearing/Self_Clearing_Server/{timelapse_directory}.zip"
        if os.path.exists(zip_path):
            print(f"removed zip file: {timelapse_directory}.zip")
            os.remove(zip_path)
        video_path = "/home/self-clearing/Self_Clearing_Server/Timelapse_Videos/" + timelapse_directory + ".mp4"
        print(video_path)
        if os.path.exists(video_path):
            print(f"removed video: {timelapse_directory}.mp4")
            os.remove(video_path)
    else:
        socketio.emit("invalid-directory", namespace="/home")

def shutdown(is_critical=False):
    pass