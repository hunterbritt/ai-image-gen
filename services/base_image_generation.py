from typing import Dict, Any
import requests
import os
import random

from utils.load_json import _log_response_data


from dotenv import load_dotenv
load_dotenv()





def _base_image_generation(api_key: str, prompt: str, **kwargs) -> Dict[str, Any]:
    modelVersion: str = kwargs.get('modelVersion', "2.2")
    numResults: int = kwargs.get('numResults', 1)
    sync: bool = kwargs.get('sync', "true")
    aspectRatio: str = kwargs.get("aspectRatio", "16:9")

    url = f"{os.getenv("BASE_IMAGE_URL")}{modelVersion}"

    headers = {
        "Content-Type": "application/json",
        "api_token": api_key
    }

    data = {
        "prompt": prompt,
        "num_results": numResults,
        "sync": sync,


        # Default/Other properties.
        # "prompt_enhancement": "true",
        "enhance_image": "true",
    }

    if aspectRatio is not None:
        data['aspect_ratio'] = aspectRatio
    data['seed'] = random.randint(30, 50)

    try:
        response = requests.post(url, json=data, headers=headers)
        responseData = response.json()
        # save the response as JSON.
        _log_response_data(prompt=prompt, data=responseData, logFileName="base")
        return responseData
    except requests.exceptions.HTTPError as e:
        print(f"Error occured when sending request. \n Error Log: {e}")
    