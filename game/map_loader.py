# --------------------------
# FILE: map_loader.py
# Purpose: Load level maps from /maps directory
# --------------------------

import os

def load_map(level_number, base_path="maps"):
    """
    Load a map file for the given level number from the specified directory.

    Args:
        level_number (int): Level identifier (e.g., 1, 2, 3...)
        base_path (str): Folder where .map files are stored

    Returns:
        List[str]: Map as list of text lines

    Raises:
        ValueError: If map file not found or format invalid
    """
    filename = os.path.join(base_path, f"level_{level_number}.map")
    if not os.path.exists(filename):
        raise ValueError(f"Map for level {level_number} not found: {filename}")

    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.strip("\n") for line in f if line.strip()]
        if not lines:
            raise ValueError(f"Map file {filename} is empty or invalid.")
        return lines
