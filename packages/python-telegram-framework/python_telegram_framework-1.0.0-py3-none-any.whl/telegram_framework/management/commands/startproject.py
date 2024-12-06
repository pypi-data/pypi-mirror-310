import os
import sys
import subprocess

from telegram_framework.utils.version import is_valid_python_version
from telegram_framework.management.base import CommandError
from telegram_framework.management.templates import TemplateCommand


class Command(TemplateCommand):
    help = "Command to create new projects"
    template_name = "project_template"
    
    def __init__(self, argv=None):
        super().__init__(argv)
        
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('-v', '--python-version', type=str, help='Python version to use in the project (must be >= 3.8).')
    
    def modify_pipfile(self, destination, python_version):
        pipfile_path = os.path.join(destination, 'Pipfile')
        if os.path.exists(pipfile_path) and python_version:
            with open(pipfile_path, 'a') as file:
                file.write(f'\n[requires]\npython_version = "{python_version}"\n')
                
    def ask_project_installation(self, destination):
        """ Ask user if want to run "pipenv install" command """
        install_dependencies = input("Would you like to create a virtual environment and install project dependencies now? (y/n): ").strip().lower()
        if install_dependencies == 'y':
            try:
                subprocess.check_call(['pipenv', 'install'], cwd=destination)
                print("Dependencies installed successfully.")
            except subprocess.CalledProcessError as e:
                print("Error installing dependecies:", e)
                sys.exit(1)
    
    def handle(self, **options):
        name = options.get('name')
        python_version = options.get('python_version', None)
        
        if python_version and not is_valid_python_version(python_version):
            raise CommandError("Python version must be 3.8 or higher.")
        
        destination = os.path.join(os.getcwd(), name)
        self.copy_template(destination)
        
        # if python_version:
        #     #TODO: preguntar si quieren un nuevo entorno virtual con pipenv, y solo si dicen que sí, añadir el Pipfile
        #     self.modify_pipfile(destination, python_version)
        
        print(f"Project '{name}' created successfully at {destination}\n")
        
        # self.ask_project_installation(destination)
