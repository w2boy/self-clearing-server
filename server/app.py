"""The app module, containing the app factory function."""
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, render_template
from server.extensions import socketio
from server.views import home, camera_1, camera_2, camera_3, camera_4, server_logs, data_collection
from server.settings import ProdConfig, DevConfig
from server.logging_handler import configure_loggers
from flask.helpers import get_debug_flag

def create_app(config_object=DevConfig):
    """An application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    # register_hardware(app)
    register_logger(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    socketio.init_app(app)


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(home.blueprint)
    app.register_blueprint(camera_1.blueprint)
    app.register_blueprint(camera_2.blueprint)
    app.register_blueprint(camera_3.blueprint)
    app.register_blueprint(camera_4.blueprint)
    app.register_blueprint(server_logs.blueprint)

def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return render_template("{}.html".format(error_code), msg=error), error_code

    for errcode in [404, 500]:
        app.errorhandler(errcode)(render_error)

# def register_hardware(app):
#     app.driver_handles = driver_handles


def register_logger(app):
    if not app.debug:
        configure_loggers(app)

CONFIG = ProdConfig
# CONFIG = DevConfig
app = create_app(CONFIG)