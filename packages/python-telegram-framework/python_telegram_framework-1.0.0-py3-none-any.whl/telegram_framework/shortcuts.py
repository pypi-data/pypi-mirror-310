from telegram_framework.conf import settings

def debug_mode_enabled():
    """Convenient way to check if debug mode is enabled"""
    return settings.DEBUG
