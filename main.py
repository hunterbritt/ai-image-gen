# Core imports
import os
# import requests
# Prompt Enhancement Imports
from services.prompt_enhancer import _enhance_prompt

# Image Generations Imports
from services.hd_image_generation import _hd_image_generation

from dotenv import load_dotenv
load_dotenv()

API_KEY = f"{os.environ.get("BRIA_API_KEY", "")}"

def main():
    userPrompt = input("Enter Prompt Here: ")
    enhancedPrompt = _enhance_prompt(api_key=API_KEY, prompt=userPrompt)
    _hd_image_generation(api_key=API_KEY, prompt=enhancedPrompt, model_version="2.2", num_of_genertions=1)

if __name__ == "__main__":
    main()