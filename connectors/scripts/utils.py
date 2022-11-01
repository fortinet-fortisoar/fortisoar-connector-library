import os
import base64


def get_dir_name(file: str) -> str:
    """Get default output path"""
    return os.path.dirname(file)


def is_path_exist(path: str) -> bool:
    """Check whether file exist or not"""
    return os.path.exists(path)


def create_path(path: str) -> bool:
    """Create path if not exist"""
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except IOError as e:
        return False


def decode_base64(data: str) -> str:
    return base64.b64decode(data).decode()
