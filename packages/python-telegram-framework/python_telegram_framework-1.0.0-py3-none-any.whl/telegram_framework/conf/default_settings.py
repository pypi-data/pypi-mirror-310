import logging

# Telegram Bot configuration
TELEGRAM_BOT_TOKEN = ''

# Project configuration
DEBUG = True

MODULES_DIR = 'modules'
# HANDLERS_MODULE = 'handlers'

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

# Logging configuration
LOGGING_LEVEL = logging.INFO # With DEGUG enabled, level is always DEBUG
LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
