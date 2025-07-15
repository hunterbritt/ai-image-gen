import os
import requests
import logging
from dotenv import load_dotenv
from typing import Dict, Any
from pathlib import Path
import json

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

def _enhance_prompt(api_key: str, prompt: str, **kwargs) -> str:
    """
    Enhance a given prompt by sending a POST request to the enhancement service.
    Args:
        api_key: API key for authentication.
        prompt: The original prompt to enhance.
        kwargs: Additional parameters to customize the prompt enhancement.

    Returns:
        Enhanced prompt or the original prompt if an error occurs.
    """
    url = os.getenv('ENHANCE_PROMPT_URL')

    if not url:
        logger.error("Enhance prompt URL is missing.")
        return prompt

    payload = {
        "prompt": prompt,
        **kwargs,
    }

    headers = {
        "Content-Type": "application/json",
        "api_token": api_key,
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        data = response.json()

        data = data.get("prompt variations")

        # Save the response data to a log file
        _log_response_data(prompt=prompt, data=data)

        return data

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request error occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")

    return prompt

def _log_response_data(prompt: str, data: Any):
    log_file_path = "services/log.json"
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    
    # Generate id based on the length
    new_id = str(int(os.path.getsize(log_file_path)) + 1 if os.path.exists(log_file_path) else 1)

    # Initializing the format.
    log_format = {
        'id': new_id,
        'userPrompt': prompt,
        'enhancedPrompt': data
    }

    try:
        with open(log_file_path, "a") as f:
            f.write(json.dumps([log_format], indent=4))
            f.write("\n")
            f.close()
        logger.info(f"Enchancement Done. check {log_file_path}")
    except json.JSONDecodeError:
        logger.error(f"Failed to enhance prompt")
    except Exception as e:
        logger.error(f"Action faile due to {e}")