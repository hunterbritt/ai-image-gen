# Core imports
import os, requests, json

# Prompt Enhancement Imports
from services.prompt_enhancer import _enhance_prompt

from dotenv import load_dotenv
load_dotenv()

API_KEY = f"{os.environ.get("BRIA_API_KEY", "")}"

def main():
    userPrompt = input("Enter Prompt Here: ")
    _enhance_prompt(api_key=API_KEY, prompt=userPrompt)

if __name__ == "__main__":
    main()