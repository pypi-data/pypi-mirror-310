import os
import sys
import subprocess


def test_createmodule_command(temporary_project):
    project_dir = temporary_project.get('project_dir', None)
    assert project_dir is not None
        
    # Run the "createmodule" command with a module name
    module_name = 'module_test'
    os.chdir(project_dir)
    result = subprocess.run(
        [sys.executable, 'manage.py', 'createmodule', module_name],
        capture_output=True,
        text=True,
    )
    
    # Check if the command runs successfully
    assert result.returncode == 0
    
    # Check if the module directory exists
    module_dir = os.path.join(project_dir, 'modules', module_name)
    os.path.exists(module_dir)
    os.path.isdir(module_dir)
    
    # Check if handlers and models files exist
    handlers_file = os.path.join(module_dir, 'handlers.py')
    assert os.path.exists(handlers_file)
    assert os.path.isfile(handlers_file)
    
    models_file = os.path.join(module_dir, 'models.py')
    assert os.path.exists(models_file)
    assert os.path.isfile(models_file)
    
    