from typing import Any
import os
import json
import logging
import time



# setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


def _log_response_data(prompt: str, data: Any, **kwargs):
    file_name = kwargs.get('logFileName', "log")
    log_file_path = f"services/{file_name}.json"

    existing_data = []
    if os.path.exists(log_file_path):
        try:
            with open(log_file_path, "r") as f:
                existing_data = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Error occured reading the JSON file {e}")
            existing_data = []
    else:
        logger.error("JSON file does not Exist \n Do you want to create it (Y/n)?")
        time.sleep(3)
        userInput = input("").lower()
        if userInput == "y":
            with open(log_file_path, "w") as f:
                json.dump(existing_data, f , indent=4)
                logger.info(f"File {log_file_path} has been created")
            # create the file
        else:
            logger.info("You declined the file creation.")
    
    # Generate id based on the length
    new_id = str(len(existing_data) + 1)

    # Initializing the format.
    log_format = {
        'id': new_id,
        'userPrompt': prompt,
        'enhancedPrompt': data
    }

    existing_data.append(log_format)

    try:
        with open(log_file_path, "w") as f:
            json.dump(existing_data, f, indent=4)
            f.write("\n")
            f.close()
        logger.info(f"Enchancement Done. check {log_file_path}")
    except json.JSONDecodeError:
        logger.error("Failed to enhance prompt")
    except Exception as e:
        logger.error(f"Action faile due to {e}")