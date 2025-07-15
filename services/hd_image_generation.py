import requests
import os
from dotenv import load_dotenv

load_dotenv()

from utils.load_json import _log_response_data


def _hd_image_generation(api_key: str, prompt: str, **kwargs):
    model_version: str  = kwargs.get('model_version', "2.2")
    numberOfGenerations: int = kwargs.get('num_of_genertions', 1)

    url = f"{os.getenv("HD_IMAGE_URL")}{model_version}"

    payload = {
        'prompt': prompt,
        'num_results': numberOfGenerations,
        'sync': True
    }

    headers = {
        "Content-Type": "application/json",
        "api_token": api_key
    }
    
    response = requests.post(url, json=payload, headers=headers)

    data = response.json()

    _log_response_data(prompt=prompt, data=data, logFileName="HD.json")

    # print(data)