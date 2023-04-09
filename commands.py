#!/usr/bin/env python
"""
This python file is an utility for commands common to `client.py` and `server.py`.
"""

import webbrowser

__author__ = "Folfy Blue"
__license__ = "GPLv3"


def connect(ip: str = "", password: str = ""):
    """Connects to the given game server IP

    Args:
        ip (str): ip to connect to, including the port
        password (str, optional): Password of the server, if any. Defaults to nothing.
    """
    webbrowser.open_new(f"steam://connect/{ip}/{password}")


def run_game(id: str = ""):
    """Runs a game given its ID

    Args:
        id (str): Game ID
    """
    webbrowser.open_new(f"steam://rungameid/{id}")
