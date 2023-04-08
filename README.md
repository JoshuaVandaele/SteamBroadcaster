# Steam Broadcaster

A Python-based multi-client server and client scripts that allow clients to connect and receive messages from the server. The server can send commands to the clients, such as connecting to a game server or running a Steam game. The clients can handle commands and execute them accordingly.

## Getting Started

Clone the repository to your local machine.

```bash
git clone https://github.com/FolfyBlue/SteamBroadcaster.git
cd SteamBroadcaster
```

## Prerequisites

Python 3.6 or higher

## Usage

Start the server by running the server.py script with a specified port number.

```bash
python server.py --port 12345
```

Start the clients by running the client.py script with the server's IP address and port number.

```bash
python client.py --host 127.0.0.1 --port 12345
```

Type messages in the server's console to broadcast them to all connected clients.

Type commands in the server's console to execute them on the clients. The following commands are available:

* `connect IP:PORT` - Connects every client to the given Valve server.
* `rungame ID` - Starts up a Steam game given its ID.
* `stop` - Stops the client script and disconnects the client from the server.
* `quit` or `exit` - Shuts down the server and disconnects all clients.

## License

This project is licensed under the GPLv3 License - see the LICENSE file for details.
