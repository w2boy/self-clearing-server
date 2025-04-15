
$(document).ready(function () {
    var socket = io.connect("http://" + document.domain + ":" + location.port + "/home");
    socket.emit("connected");
    console.log("home ready");

    $("#download-timelapse-pics-btn").click(function () {
        timelapse_directory_field = document.getElementById("timelapse-directory");
        timelapse_directory = timelapse_directory_field.value;
        socket.emit("prepare-directory", {"timelapse-directory": timelapse_directory});
    });

    socket.on("download-ready", function(timelapse_directory) {
        window.location.href = "/download/" + timelapse_directory;
    });

    socket.on("invalid-directory", function() {
        alert("That timelapse folder doesn't exist!");
    });

    $("#create-and-download-timelapse-video-btn").click(function () {
        timelapse_directory_field = document.getElementById("timelapse-directory");
        timelapse_directory = timelapse_directory_field.value;
        socket.emit("prepare-video", {"timelapse-directory": timelapse_directory});
    });

    socket.on("video-download-ready", function(video_name) {
        window.location.href = "/download_video/" + video_name;
    });

    $("#delete-directory-btn").click(function () {
        timelapse_directory_field = document.getElementById("timelapse-directory");
        timelapse_directory = timelapse_directory_field.value;
        socket.emit("delete-directory", {"timelapse-directory": timelapse_directory});
    });

});