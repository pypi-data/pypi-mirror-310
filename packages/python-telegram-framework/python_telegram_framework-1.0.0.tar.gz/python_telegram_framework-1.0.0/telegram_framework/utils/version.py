from packaging.version import parse as parse_version


def is_valid_python_version(version):
    """Check if the Python version is valid for the project (for compatibility with python-telegram-bot package)"""
    return parse_version(version) >= parse_version("3.8")
