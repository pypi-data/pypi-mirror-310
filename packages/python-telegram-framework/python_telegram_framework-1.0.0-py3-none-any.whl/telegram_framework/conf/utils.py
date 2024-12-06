import os
import sys

def initialize_settings(path = __file__, project_module = 'settings'):
    os.environ.setdefault('TELEGRAM_SETTINGS_MODULE', project_module)
    if path not in sys.path: sys.path.insert(0, path)
