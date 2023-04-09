#!/usr/bin/env python
"""
This Python file attempts to connect to a server on a specific host and port,
and receives messages from the server until it receives the "stop" message or the user interrupts the program.

Usage: `python client.py --host HOST --port PORT`
Example: `python client.py -h 107.0.0.1 -p 42069`
> Attempting to connect...
> Connected to 107.0.0.1:42069!
"""

import argparse
import socket
import webbrowser
from time import sleep
from typing import Callable

__author__ = "Folfy Blue"
__license__ = "GPLv3"

client_socket: socket.socket


def command_handler(msg: str):
    """Handles messages received by the server

    Args:
        msg (str): message to handle
    """
    global COMMANDS
    for cmd in COMMANDS:
        if msg.startswith(cmd):
            print(f"Executing command `{msg}`")
            args: list[str] = msg[len(cmd) :].split()
            COMMANDS[cmd](*args)
            return
    print(f"Received message: {msg}")


def connect(ip: str):
    """Connects to the given game server IP

    Args:
        ip (str): ip to connect to, including the port
    """
    webbrowser.open_new(f"steam://connect/{ip}")


def run_game(id: str):
    """Runs a game given its ID

    Args:
        id (str): Game ID
    """
    webbrowser.open_new(f"steam://rungameid/{id}")


def graceful_exit():
    """Disconnects the client from the server"""
    global client_socket
    print("Disconnecting from the server...")
    client_socket.close()
    quit()


COMMANDS: dict[str, Callable] = {
    "connect": connect,
    "rungame": run_game,
    "stop": graceful_exit,
    "quit": graceful_exit,
    "exit": graceful_exit,
}


def main(host: str, port: int):
    """Connects to a server and receives messages.

    This function attempts to connect to a server on a specific host and port. If the connection
    is successful, it receives messages from the server until it receives the "stop" message or
    the user interrupts the program.

    The function will retry connecting to the server up to a maximum number of attempts with a
    timeout between retries.

    Args:
        host (str): Host to use
        port (int): Port to use
    """
    global client_socket
    maximum_connection_attempts: int = 5
    retry_timeout: int = 1

    attempts: int = 0
    print("Attempting to connect...")
    while attempts < maximum_connection_attempts:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))
            break
        except ConnectionRefusedError:
            attempts += 1
            print(
                f"Connection refused, retrying... ({attempts}/{maximum_connection_attempts})"
            )
            sleep(retry_timeout)
    else:
        print(f"Failed to connect to {host}:{port}!")
        return
    print(f"Connected to {host}:{port}!")
    client_socket.settimeout(1)

    message: str = ""
    try:
        while True:
            try:
                message = client_socket.recv(1024).decode()
                command_handler(message)
            except socket.timeout:
                continue
    except KeyboardInterrupt:
        graceful_exit()


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Connects to a server and receives messages.", add_help=False
    )
    parser.add_argument(
        "--host", "-h", required=True, help="The server's hostname or IP address."
    )
    parser.add_argument(
        "--port",
        "-p",
        required=False,
        type=int,
        help="The server's port. (default: 42069)",
        default=42069,
    )
    args = parser.parse_args()
    main(args.host, args.port)
