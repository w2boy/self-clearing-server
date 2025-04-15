$(document).ready(function () {
    var socket = io.connect("http://" + document.domain + ":" + location.port + "/camera_1");
    var socket = io("/camera_1");  // This ensures connection to the correct namespace

    socket.emit("connected");
    console.log("camera_1 ready");

    const turn_on_camera_btn = document.getElementById('turn-on-camera-btn');
    const turn_off_camera_btn = document.getElementById('turn-off-camera-btn');
    const start_timelapse_btn = document.getElementById('start-timelapse-btn');
    const stop_timelapse_btn = document.getElementById('stop-timelapse-btn');

    socket.on("connect", function() {
        console.log("Connected to /camera_1 namespace");
        socket.emit("initialize-buttons"); // Emit the request when connected
    });

    socket.on("camera_states", function(camera_states){
        console.log("Received camera states:", camera_states);  // Debugging

        let camera_is_on = camera_states[0]
        let timelapse_is_on = camera_states[1]

        // Update button states based on camera status
        turn_on_camera_btn.disabled = camera_is_on;
        turn_off_camera_btn.disabled = !camera_is_on;
        start_timelapse_btn.disabled = timelapse_is_on;
        stop_timelapse_btn.disabled = !timelapse_is_on;

    });

    // Listen for updates from server and enable or disable buttons
    socket.on("disable-on-button", function() {
        turn_on_camera_btn.disabled = true;
        turn_off_camera_btn.disabled = false;
    });

    socket.on("disable-off-button", function() {
        turn_off_camera_btn.disabled = true;
        turn_on_camera_btn.disabled = false;
    });

    socket.on("disable-timelapse-on-btn", function() {
        start_timelapse_btn.disabled = true;
        stop_timelapse_btn.disabled = false;
    });

    socket.on("disable-timelapse-off-btn", function() {
        start_timelapse_btn.disabled = false;
        stop_timelapse_btn.disabled = true;
    });

    $("#stop-timelapse-btn").click(function () {
        socket.emit("stop-timelapse");
    });

    $("#start-timelapse-btn").click(function () {
        inputField = document.getElementById("timelapse-name-1");
        timelapse_duration_field = document.getElementById("timelapse-duration");
        timelapse_frequency_field = document.getElementById("timelapse-frequency");
        value = inputField.value;
        timelapse_duration = timelapse_duration_field.value;
        timelapse_frequency = timelapse_frequency_field.value;
        socket.emit("start-timelapse", {"timelapse-name-1": value, "timelapse-duration": timelapse_duration, "timelapse-frequency": timelapse_frequency});
    });

    $("#turn-off-camera-btn").click(function () {
        socket.emit("turn-off-camera");
    });

    $("#turn-on-camera-btn").click(function () {
        socket.emit("turn-on-camera");
    });

    // window.addEventListener('load', () => {
    //     const turn_on_camera_btn_state = localStorage.getItem('turn_on_camera_btn_state');
    //     const turn_off_camera_btn_state = localStorage.getItem('turn_off_camera_btn_state');
    //     const start_timelapse_btn_state = localStorage.getItem('start_timelapse_btn_state');
    //     const stop_timelapse_btn_state = localStorage.getItem('stop_timelapse_btn_state');
    //     if (turn_on_camera_btn_state === 'disabled') {
    //         turn_on_camera_btn.disabled = true;
    //     }
    //     if (turn_off_camera_btn_state === 'disabled') {
    //         turn_off_camera_btn.disabled = true;
    //     }
    //     if (start_timelapse_btn_state === 'disabled') {
    //         start_timelapse_btn.disabled = true;
    //     }
    //     if (stop_timelapse_btn_state === 'disabled') {
    //         stop_timelapse_btn.disabled = true;
    //     }
    // });

    // turn_on_camera_btn.addEventListener('click', () => {
    //     turn_on_camera_btn.disabled = true;
    //     turn_off_camera_btn.disabled = false;
    //     localStorage.setItem('turn_on_camera_btn_state', 'disabled');
    //     localStorage.setItem('turn_off_camera_btn_state', 'enabled');
    // });

    // turn_off_camera_btn.addEventListener('click', () => {
    //     turn_on_camera_btn.disabled = false;
    //     turn_off_camera_btn.disabled = true;
    //     localStorage.setItem('turn_on_camera_btn_state', 'enabled');
    //     localStorage.setItem('turn_off_camera_btn_state', 'disabled');
    // });

    // start_timelapse_btn.addEventListener('click', () => {
    //     start_timelapse_btn.disabled = true;
    //     stop_timelapse_btn.disabled = false;
    //     localStorage.setItem('start_timelapse_btn_state', 'disabled');
    //     localStorage.setItem('stop_timelapse_btn_state', 'enabled');
    // });

    // stop_timelapse_btn.addEventListener('click', () => {
    //     start_timelapse_btn.disabled = false;
    //     stop_timelapse_btn.disabled = true;
    //     localStorage.setItem('stop_timelapse_btn_state', 'disabled');
    //     localStorage.setItem('start_timelapse_btn_state', 'enabled');
    // });
});

function getValue() {
    // Get the input element by its ID
    let inputField = document.getElementById("timelapse-name-1");

    // Get the value of the input field
    let value = inputField.value;

    // Display the value in an alert
    // alert("Input value: " + value);
}