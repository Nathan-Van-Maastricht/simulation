import json


def load_config(config_file_path):
    with open(config_file_path, "r") as file:
        config = json.load(file)
    return config


config_file_path = "config.json"
config = load_config(config_file_path)

print(config)
