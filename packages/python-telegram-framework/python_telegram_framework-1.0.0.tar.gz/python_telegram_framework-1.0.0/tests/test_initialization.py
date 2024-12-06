import os

from telegram_framework.conf import settings

def test_initialized_project(temporary_project):
    project_dir = temporary_project.get('project_dir', None)
    assert project_dir is not None
    
    # Check if app, manage, settings, and models files are present
    app_file = os.path.join(project_dir, 'app.py')
    manage_file = os.path.join(project_dir, 'manage.py')
    settings_file = os.path.join(project_dir, 'settings.py')
    callbacks_file = os.path.join(project_dir, 'models.py')
    assert (
        os.path.isfile(app_file) and 
        os.path.isfile(manage_file) and 
        os.path.isfile(settings_file) and
        os.path.isfile(callbacks_file)
    )
    
    # Check if settings module is invocable, and BASE_DIR is correct
    base_dir = getattr(settings, 'BASE_DIR', None)
    assert base_dir is not None
    assert os.path.samefile(base_dir, project_dir)
