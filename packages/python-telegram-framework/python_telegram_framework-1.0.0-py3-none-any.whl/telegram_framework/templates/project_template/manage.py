"""Command-line utility for administrative tasks."""
import os
import sys

from telegram_framework.conf.utils import initialize_settings


def main():
    """Run administrative tasks."""
    
    # 'project_module' parameter can be modified if you are using multiple settings files (development, production...)
    initialize_settings(__file__)
    
    try:
        from telegram_framework.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Telegram Framework. Did you "
            "forget to activate a virtual environment or install all dependencies?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
