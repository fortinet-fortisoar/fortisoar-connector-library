""" Copyright start
  Copyright (C) 2008 - 2024 Fortinet Inc.
  All rights reserved.
  FORTINET CONFIDENTIAL & FORTINET PROPRIETARY SOURCE CODE
  Copyright end """

import os
import base64
import json


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


def read_local_data(local_data_path: str) -> dict:
    data = {}
    with open(local_data_path, "r") as fp:
        # if local data is encoded
        # content = decode_base64(fp.read())
        data = json.load(fp)
    return data


def write_local_data(local_data_path: str, local_data: dict) -> None:
    with open(local_data_path, "w") as fp:
        fp.write(json.dumps(local_data, indent=2))
        fp.close()
