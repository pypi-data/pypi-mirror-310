import os
import shutil
from abc import ABC, abstractmethod

import telegram_framework
from .base import BaseCommand, CommandError


class TemplateCommand(BaseCommand, ABC):
    @property
    @abstractmethod
    def template_name(self):
        pass
    
    @property
    def template_directory(self):
        return os.path.join(telegram_framework.__path__[0], 'templates', self.template_name)
    
    def __init__(self, argv=None):
        super().__init__(argv)

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Name of the project or module')
        #TODO: extra argument opcional para indicar la ruta concreta donde se quiere crear la template (--directory/-d)
        
    def copy_template(self, destination):
        if not os.path.exists(self.template_directory):
            raise CommandError("The template being attempted to copy does not exist.")
        
        if os.path.exists(destination):
            raise CommandError(f"The destination directory '{destination}' already exists.")
            
        os.makedirs(destination)
        
        for item in os.listdir(self.template_directory):
            src = os.path.join(self.template_directory, item)
            dst = os.path.join(destination, item)
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
