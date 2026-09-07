"""Small JSON persistence layer for the local habit tracker."""  # Describe this module.

import json  # Encode and decode the JSON store.
import os  # Read the configurable storage path.
from typing import Any, Dict  # Describe the JSON object shape.

DATA_FILE = os.getenv("STORAGE_PATH", "./data/habit_store.json")  # Select the configured data file.


def load_data() -> Dict[str, Any]:  # Load the store or return an empty object.
    if not os.path.exists(DATA_FILE):  # Detect a first application run.
        directory = os.path.dirname(DATA_FILE)  # Find the parent directory.
        if directory:  # Avoid creating an empty path.
            os.makedirs(directory, exist_ok=True)  # Create the storage directory.
        with open(DATA_FILE, "w", encoding="utf-8") as file:  # Create the empty JSON file.
            json.dump({}, file)  # Initialize the file with an object.
        return {}  # Return the empty store.
    with open(DATA_FILE, "r", encoding="utf-8") as file:  # Open the existing store.
        try:  # Handle malformed JSON safely.
            value = json.load(file)  # Decode the JSON document.
        except json.JSONDecodeError:  # Recover from a corrupted or empty file.
            return {}  # Return a clean in-memory store.
    return value if isinstance(value, dict) else {}  # Enforce the expected object shape.


def save_data(data: Dict[str, Any]) -> None:  # Persist the complete store.
    directory = os.path.dirname(DATA_FILE)  # Find the parent directory.
    if directory:  # Avoid creating an empty path.
        os.makedirs(directory, exist_ok=True)  # Create the storage directory.
    with open(DATA_FILE, "w", encoding="utf-8") as file:  # Open the store for replacement.
        json.dump(data, file, indent=2)  # Write readable JSON.
