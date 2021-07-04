# Overview

This server runs a chatroom between multiple clients with commands to transfer files from the server to the clients. I built it to deepen my knowledge of server client networking as well as threading.

The program works by opening a terminal window and running server.py. The server will then listen for connections. Adding a connection is as simple as running client.py. When a client script is ran it will ask the user for a nickname and it will inform all other users on the server that the client has joined. The clients can then freely chat to each other by typing in the therminal. If a client wishes to recieve the cat photo all they have to do is type '**CAT**' in the chat and it will be sent to them.

I wrote this software out of a fascination for networking and the power that it has in software. I hope to keep expanding on it and make a server that will allow me to communicate with my peers and send files between each other.

[Software Demo Video](https://youtu.be/xmYiqbO-97A)

# Network Communication

The server runs server to client. This means that the clients can communicate to each other through the server which handles all the logic and communication. The clients never directly talk to one another

I am using TCP and I used port number 65432 to send and recieve data on my computer using local host

# Development Environment

* Python 3.8.2
* socket
* threading
* Visual Studio Code
* Git / Github

# Useful Websites

{Make a list of websites that you found helpful in this project}
* [Python socket tutorial](https://pythonprogramming.net/sockets-tutorial-python-3/)
* [Network file transfer tutorial (Python)](https://www.thepythoncode.com/article/send-receive-files-using-sockets-python)

# Future Work

* Add quality of life features like quiting and seeing every active user in the server
* Add a feature for clients to send files between each other
* Add a feature for more types of files to be sent