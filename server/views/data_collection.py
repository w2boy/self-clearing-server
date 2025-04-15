import logging
from flask import Blueprint, render_template, send_file

from server.settings import Config

blueprint = Blueprint(
    "data_collection", __name__, url_prefix="/", static_folder="../static"
)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


@blueprint.route("/data_collection")
def index():
    return render_template("data_collection.html", hostname=Config.HOSTNAME)
