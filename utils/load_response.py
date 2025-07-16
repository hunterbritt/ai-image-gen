import json
import os
import sys

def load_api_response(log_name="base", folder="services"):
    """
    Load the JSON file that _log_response_data wrote.
      - log_name: the `logFileName` you passed ("base" → "services/base.json")
      - folder: directory where you store your logs
    Returns the parsed JSON (list or dict), or None on failure.
    """
    path = os.path.join(folder, f"{log_name}.json")
    if not os.path.exists(path):
        print(f"[Error] Log file not found: {path}", file=sys.stderr)
        return None

    try:
        with open(path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"[Error] Failed to parse JSON from {path}: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"[Error] Unexpected error reading {path}: {e}", file=sys.stderr)
        return None
