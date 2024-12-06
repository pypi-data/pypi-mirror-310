""" Global fixtures available for all test functions """

import os
import shutil
import pytest

from telegram_framework.management import execute_from_command_line
from telegram_framework.conf.utils import initialize_settings

import logging

LOGGER = logging.getLogger(__name__)

@pytest.fixture(scope="session")
def temporary_project(tmp_path_factory):
    """Fixture to initialize a project using the framework."""
    
    temp_path = tmp_path_factory.mktemp("test")
    project_name = "test_project"
    
    # Change to temporary directory
    original_cwd = os.getcwd()
    os.chdir(temp_path)
    
    try:
        # Create temporary project with "startproject" command
        execute_from_command_line(['python-telegram-framework', 'startproject', project_name], debug=True)
        project_dir = os.path.join(temp_path, project_name)

        # Check that the project was created successfully
        assert os.path.exists(project_dir)
        assert os.path.isdir(project_dir)
        
        initialize_settings(project_dir)
        
        yield {
            'project_dir': project_dir
        }
        
    finally:
        # Return to the original working directory
        os.chdir(original_cwd)
        shutil.rmtree(temp_path)
