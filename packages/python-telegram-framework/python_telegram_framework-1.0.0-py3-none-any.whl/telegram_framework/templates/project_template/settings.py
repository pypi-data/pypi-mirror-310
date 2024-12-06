"""
Settings for this telegram framework project.

For the full list of settings and their values, see:
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

# Telegram Bot configuration
TELEGRAM_BOT_TOKEN = ''

# Project configuration
DEBUG = True

# Webhook configuration
USE_WEBHOOK = False
WEBHOOK_LISTEN = '127.0.0.1'
WEBHOOK_PORT = 5000
WEBHOOK_URL_PATH = ""
WEBHOOK_URL = None # If None: "http(s)://<WEBHOOK_LISTEN>:<WEBHOOK_PORT>/<WEBHOOK_URL_PATH>" by default
WEBHOOK_IP_ADDRESS = None
WEBHOOK_SECRET_TOKEN = None
WEBHOOK_CERT = None
WEBHOOK_SSL_KEY = None

USE_NGROK = False
NGROK_TOKEN = ''
NGROK_REGION = 'eu'
