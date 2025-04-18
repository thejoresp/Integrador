import os
import uuid
from typing import Set

def generate_unique_id():
    """Genera un identificador único para operaciones."""
    return str(uuid.uuid4())

def allowed_file(filename: str, allowed_extensions: Set[str]):
    """Verifica si la extensión del archivo está permitida."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def ensure_directory(directory_path: str):
    """Asegura que un directorio exista."""
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
