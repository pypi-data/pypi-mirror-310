import requests
from .flames import flames_game
from .xo import xo

def get_version_from_pypi():
    """Fetch the latest version of the rupi library from PyPI."""
    try:
        response = requests.get("https://pypi.org/pypi/rupi/json", timeout=5)
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.json()
        return data["info"]["version"]
    except Exception:
        return "Unknown (Could not fetch from PyPI)"

def get_about_message():
    version = get_version_from_pypi()
    about_message = f"""
    Rupi Library:
    This library implements:
    1. FLAMES game: A fun relationship game based on two names.
    2. XO (Tic-Tac-Toe) game: A GUI-based game for two players built with Tkinter.

    PyPI: https://pypi.org/project/rupi/
    Author: Tanujairam
    Email: tanujairam.v@gmail.com
    Version: {version}
    """
    return about_message
