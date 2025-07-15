import os
import requests
import logging
from dotenv import load_dotenv


from utils.load_json import _log_response_data

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

    return data

