from datetime import date
import logging
import logging.config
import json


with open("config/logging.json", "r") as f:
    config = json.load(f)

    log_file_pattern = config["handlers"]["file"]["filename"].format(
        asctime=date.today()
    )
    config["handlers"]["file"]["filename"] = log_file_pattern

    logging.config.dictConfig(config)
