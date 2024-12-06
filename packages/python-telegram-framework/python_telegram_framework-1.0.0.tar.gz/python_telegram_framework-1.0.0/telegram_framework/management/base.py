import os
import sys
import argparse
from abc import ABC, abstractmethod


class CommandError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
    
    def __str__(self):
        return f"CommandError: {self.message}"


class BaseCommand(ABC):
    @property
    @abstractmethod
    def help(self):
        pass
    
    def __init__(self, argv=None):
        self.argv = argv or sys.argv
        script_name = os.path.basename(self.argv[0])
        if script_name == "__main__.py":
            script_name = "python -m telegram_framework"
        command_name = self.argv[1]
        prog = f'{script_name} {command_name}'
        
        self.parser = argparse.ArgumentParser(
            description=self.help,
            prog=prog,
            # usage=f'%(prog)s [options]'
        )
        self.add_arguments(self.parser)
        
    @abstractmethod
    def add_arguments(self, parser):
        pass
    
    @abstractmethod
    def handle(self, **options):
        pass
    
    def print_help(self):
        self.parser.print_help()    

    def execute(self):
        try:
            options = self.parser.parse_args(self.argv[2:])
            self.handle(**vars(options))
        except CommandError as e:
            print(e)
            self.print_help()
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            self.print_help()
