import json
import logging
from pathlib import Path
from server.settings import Config

default_log_level = logging.INFO
dummy = False


configuration_path = Path(Config.SERVER_FOLDER).joinpath('hardware_configuration').rglob("hardware_configuration.json")

with open(next(configuration_path), "r") as file_handle:
    config_dict = json.load(file_handle)

class Printer3D:
    """Provides hardware handles to the Flask print control."""

    def __init__(self):
        # Dynamically import python snippits
        global config_dict

        if "camera" in config_dict.keys():
            from server.drivers.camera import Camera

            self.camera = Camera(config_dict=config_dict["camera"], log_level=default_log_level)

            self.printer = Printer()


    def disconnect(self):
        if hasattr(self, "camera"):
            self.camera.disconnect()
        if hasattr(self, "newmark"):
            self.newmark.disconnect()
        if hasattr(self, "gpio"):
            self.gpio.disconnect()

            
driver_handles = Printer3D()
