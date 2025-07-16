# Core imports
import os
import time

# Prompt Enhancement Imports
from services.prompt_enhancer import _enhance_prompt

# Image Generations Imports

# Base Image Generations
from services.base_image_generation import _base_image_generation


# utils imports
from utils.image_preview import preview_images
from utils.load_response import load_api_response

from dotenv import load_dotenv
load_dotenv()

API_KEY = f"{os.environ.get("BRIA_API_KEY", "")}"

def main():
    userPrompt = input("Enter Prompt Here: ")

    _enhance_prompt(api_key=API_KEY, prompt=userPrompt)
    _base_image_generation(
        api_key=API_KEY, 
        prompt=userPrompt, 
        modelVersion="3.2", 
        numResults=4,
        # aspectRatio="9:16"
    )

    resp = load_api_response('base', folder="services")
    if resp is None:
        return 

    time.sleep(5)
    preview_images(api_response=resp)

if __name__ == "__main__":
    main()