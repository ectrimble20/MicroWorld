import json
import logging
import os
from localpaths import SETTINGS_FILE, MASTER_MAP_FILE


__all__ = ['read_from_json_file', 'write_json_to_file', 'load_master_map_file', 'load_settings_file']


def read_from_json_file(file_path: str) -> dict:
    with open(file_path, 'r') as handle:
        json_data = json.load(handle)
    return json_data


# TODO, this name isn't really good, it's not writing json, it's building then writing json with the json module
def write_json_to_file(json_dict: dict, file_path: str):
    with open(file_path, 'w+') as handle:
        json.dump(json_dict, handle)


def load_master_map_file() -> dict:
    # first, verify we have a master map file
    if not os.path.isfile(MASTER_MAP_FILE):
        logging.warning(f"Master map file {MASTER_MAP_FILE} was not found, building")
        write_json_to_file({"maps": []}, MASTER_MAP_FILE)
    # next, once we've verified a map file exists or we created one, read it's contents
    return read_from_json_file(MASTER_MAP_FILE)


def load_settings_file() -> dict:
    # verify we have a configuration/settings file
    if not os.path.isfile(SETTINGS_FILE):
        logging.error(f"Configuration file {SETTINGS_FILE} was not found")
        raise FileNotFoundError(f"Configuration file {SETTINGS_FILE} was not found")
    return read_from_json_file(SETTINGS_FILE)
