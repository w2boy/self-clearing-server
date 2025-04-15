"""Application configuration."""
import os
import socket


class Config:
    """Base configuration."""

    PROFILE_CODE = False
    SECRET_KEY = os.environ.get("PRINTER_SERVER_SECRET", "secret-key")  # TODO: Change me
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    UPLOAD_FOLDER = os.path.abspath(os.path.join(PROJECT_ROOT, "upload"))
    DOWNLOAD_FOLDER = os.path.abspath(os.path.join(PROJECT_ROOT, "download"))
    PROFILES_FOLDER = os.path.abspath(os.path.join(PROJECT_ROOT, "profiles"))
    SERVER_FOLDER = os.path.abspath(os.path.join(PROJECT_ROOT, "server"))
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    HOSTNAME = socket.gethostname()


class ProdConfig(Config):
    """Production configuration."""

    ENV = "prod"
    DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar


class DevConfig(Config):
    """Development configuration."""

    ENV = "dev"
    DEBUG = True
    DEBUG_TB_ENABLED = True
    CACHE_TYPE = "simple"  # Can be "memcached", "redis", etc.