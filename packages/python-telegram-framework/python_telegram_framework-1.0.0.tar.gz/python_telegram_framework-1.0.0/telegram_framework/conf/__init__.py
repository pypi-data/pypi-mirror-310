import os
import importlib

from telegram_framework.exceptions import ImproperlyConfigured
from telegram_framework.utils.functional import LazyObject
from telegram_framework.conf import default_settings

ENVIRONMENT_VARIABLE = "TELEGRAM_SETTINGS_MODULE"

class Settings:
    def __init__(self, settings_module) -> None:
        
        self.SETTINGS_MODULE = settings_module
        
        try:
            module = importlib.import_module(settings_module)
        except ImportError:
            raise ImproperlyConfigured(f"Module '{settings_module}' not found.")
        
        # Default settings are loaded first
        for setting in dir(default_settings):
            if setting.isupper():
                setattr(self, setting, getattr(default_settings, setting))
        
        # Settings from the project settings module are then loaded, overriding the default ones
        for setting in dir(module):
            if setting.isupper():
                setattr(self, setting, getattr(module, setting))


class LazySettings(LazyObject):
    def _setup(self):
        settings_module = os.environ.get(ENVIRONMENT_VARIABLE)
        if not settings_module:
            raise ImproperlyConfigured("Settings are not configured. You must define the environment variable.")
        
        self._wrapped = Settings(settings_module)
        

settings = LazySettings()
