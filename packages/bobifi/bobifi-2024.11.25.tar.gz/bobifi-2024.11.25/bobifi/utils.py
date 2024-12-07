import json


def json_load_file(filename: str):
    """Load JSON from file"""
    with open(filename) as fp:
        return json.load(fp)
