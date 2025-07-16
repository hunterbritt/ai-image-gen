# utils/image_preview.py

import sys
import requests
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


def fetch_image(url: str):
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return Image.open(BytesIO(resp.content))
    except Exception as e:
        logger.warning(f"Could not fetch {url!r}: {e}")
        return None


def single_image(image, title=None):
    plt.figure(figsize=(6, 6))
    plt.imshow(image)
    plt.axis("off")
    if title:
        plt.title(title)
    plt.show()


def display_multiple_images(images, titles=None, cols=2):
    num = len(images)
    rows = (num + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows))
    axes = axes.flatten()

    for i, img in enumerate(images):
        axes[i].imshow(img)
        axes[i].axis("off")
        if titles and i < len(titles):
            axes[i].set_title(titles[i], fontsize=8)

    for ax in axes[num:]:
        ax.axis("off")

    plt.tight_layout()
    plt.show()


def preview_images(api_response):
    # 1) Normalize to a list of "entries"
    if isinstance(api_response, list):
        entries = api_response
    elif isinstance(api_response, dict):
        # if your API wraps list under "data"
        if isinstance(api_response.get("data"), list):
            entries = api_response["data"]
        else:
            entries = [api_response]
    else:
        logger.error("Unsupported response type: %r", type(api_response))
        return

    # 2) Extract all URLs & seeds
    image_urls = []
    seeds = []
    for entry in entries:
        # drill into enhancedPrompt → result
        result_list = (
            entry.get("enhancedPrompt", {})  # top-level key
                 .get("result", [])
        )
        for r in result_list:
            urls = r.get("urls", [])
            for u in urls:
                image_urls.append(u)
                seeds.append(f"Seed: {r.get('seed', 'N/A')}")

    if not image_urls:
        logger.warning("No image URLs found in the response.")
        return

    # 3) Fetch & collect PIL images
    images = []
    valid_titles = []
    for url, title in zip(image_urls, seeds):
        img = fetch_image(url)
        if img:
            images.append(img)
            valid_titles.append(title)

    if not images:
        logger.info("No images could be downloaded.")
        return

    # 4) Display
    if len(images) == 1:
        single_image(images[0], title=valid_titles[0])
    else:
        display_multiple_images(images, titles=valid_titles, cols=2)
