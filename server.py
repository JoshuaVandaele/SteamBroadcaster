#!/usr/bin/env python
"""
This Python file is a simple server that listens on a specified IP address and port, and accepts incoming connections from clients.
When a client connects, the server adds it to a list of connected clients, and spawns a new thread to handle communication with that client.

Usage: `python server.py PORT`

Command list:
- connect IP:PORT
Connects every client to the given Valve server
- rungame ID
Starts up a steam game given it's ID
"""

import argparse
import socket
import threading
import webbrowser
from typing import Callable

__author__ = "Folfy Blue"
__license__ = "GPLv3"

connected_clients: list[socket.socket] = []
server_socket: socket.socket = None  # type: ignore
shutdown: bool = False


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
            break
    send_message_to_all_clients(msg)


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


COMMANDS: dict[str, Callable] = {
    "connect": connect,
    "rungame": run_game,
    "stop": quit,
    "quit": quit,
    "exit": quit,
}


def server_print(*args):
    """Prints a message to the server stdout with a prefix of "Broadcast > ".

    Args:
        *args: A variable number of arguments to print.
    """
    print("\r", *args, end="\nBroadcast > ", sep="")


def client_handler(client_socket, address):
    """Handles a client connection.

    This function runs in a separate thread for each connected client.
    It receives messages from the client and broadcasts them to all connected clients.

    Args:
        client_socket: A socket object representing the client's socket.
        address: A tuple representing the client's address (host, port).
    """
    global connected_clients, shutdown
    server_print(f"Client {address} connected")
    connected_clients.append(client_socket)

    try:
        while not shutdown:
            message: str
            if message := client_socket.recv(1024).decode():
                server_print(f"Message from {address}: {message}")
            else:
                break
    except Exception as e:
        server_print(f"Error: {e}")

    connected_clients.remove(client_socket)
    client_socket.close()
    server_print(f"Client {address} disconnected")


def send_message_to_all_clients(message):
    """Sends a message to all connected clients.

    Args:
        message: A string representing the message to broadcast.
    """
    global connected_clients
    for client_socket in connected_clients:
        client_socket.sendall(message.encode())


def quit():
    global server_socket
    global shutdown
    print("\nShutting down the server...")
    shutdown = True
    server_socket.close()  # type: ignore
    for client_socket in connected_clients:
        client_socket.close()


def accept_connections():
    """Accepts incoming client connections.

    This function runs in a separate thread and continuously listens for incoming client
    connections. When a connection is accepted, it spawns a new thread to handle the client.
    """
    global server_socket
    global shutdown
    while not shutdown:
        try:
            client_socket, address = server_socket.accept()  # type: ignore
            handler_thread = threading.Thread(
                target=client_handler, args=(client_socket, address)
            )
            handler_thread.daemon = True
            handler_thread.start()
        except Exception as e:
            if not shutdown:
                server_print(f"Error: {e}")


def main(port: int):
    """Starts the server and waits for user input.

    This function initializes the server socket, starts a thread to accept incoming
    client connections, and then waits for user input to broadcast messages or to run commands such as shutting down the server.

    Args:
        port (int): Port to use
    """
    global server_socket, shutdown
    host: str = "0.0.0.0"

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server listening on {host}:{port}")
    print("Press CTRL-C or type 'exit' to exit")

    accept_thread = threading.Thread(target=accept_connections, args=())
    accept_thread.daemon = True
    accept_thread.start()

    try:
        while True:
            inp = input("Broadcast > ")
            command_handler(inp)
    except KeyboardInterrupt:
        command_handler("quit")


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Connects to a server and receives messages.", add_help=False
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
    main(args.port)
