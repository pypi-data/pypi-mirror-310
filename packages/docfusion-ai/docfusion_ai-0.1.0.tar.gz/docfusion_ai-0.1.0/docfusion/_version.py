# __version__ = "0.0.1"


import toml
import os

# Get the directory of the current file
current_dir = os.path.dirname(__file__)

# Load pyproject.toml
pyproject_path = os.path.join(current_dir, "..", "pyproject.toml")
pyproject_data = toml.load(pyproject_path)

# Extract version from pyproject.toml
__version__ = pyproject_data["tool"]["poetry"]["version"]
