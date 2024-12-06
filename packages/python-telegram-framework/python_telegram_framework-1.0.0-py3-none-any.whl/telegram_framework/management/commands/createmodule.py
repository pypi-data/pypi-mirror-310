import os
import sys
import keyword

from telegram_framework.conf import settings
from telegram_framework.management.base import CommandError
from telegram_framework.management.templates import TemplateCommand


class Command(TemplateCommand):
    help = "Create a new module within the project"
    template_name = "module_template"
    
    def __init__(self, argv):
        super().__init__(argv)

    def handle(self, **options):
        name = options.get('name')
        
        if not name:
            raise ValueError("You must provide a name for the module.")
        
        if not name.isidentifier():
            raise ValueError(f"'{name}' is not a valid Python identifier.")
        
        if keyword.iskeyword(name):
            raise ValueError(f"'{name}' is a reserved Python keyword and cannot be used as a module name.")

        base_directory = os.path.join(os.getcwd(), *settings.MODULES_DIR.split('.'))
        destination = os.path.join(base_directory, name)
        
        if os.path.exists(destination):
            raise FileExistsError(f"A module named '{name}' already exists at {destination}.")
    
        self.copy_template(destination)
        
        modules_file = os.path.join(destination, "handlers.py")
        with open(modules_file, "a", encoding="utf-8") as f:
            f.write(f"\n{name} = Module('{name}', __name__)\n")
        
        print(f"Module '{name}' created successfully at {destination}\n")
