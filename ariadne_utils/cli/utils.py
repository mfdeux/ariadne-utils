import typing
import os
import shutil

# Location of package-included ticker symbols
DATA_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', '..', 'data')
NEW_SCHEMA_FILE = os.path.join(DATA_DIR, 'schema.graphql')

def generate_new_schema() -> None:
    """
    Loads list of user agents
    Args:
        filepath: path to user agent file

    Returns:
        List of user agents

    """
    shutil.copy(NEW_SCHEMA_FILE, '.')