import sys
import importlib

from telegram_framework.management.base import CommandError

def execute_from_command_line(argv=None, debug=False):
    argv = argv or sys.argv

    if len(argv) < 2:
        print("Please provide a command.")
        return

    command_name = argv[1]
    try:
        module = importlib.import_module(f'telegram_framework.management.commands.{command_name}')
        command = module.Command(argv)
        command.execute()
    except ModuleNotFoundError as e:
        print(f"Command '{command_name}' could not be found.")
        if debug: raise e
    except AttributeError as e:
        print(f"The module '{command_name}' does not have a 'Command' class.")
        if debug: raise e
    except CommandError as e:
        print(e)
        if debug: raise e
    except Exception as e:
        print(f"Unexpected error: {e}")
        if debug: raise e
