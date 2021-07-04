import socket
import threading
import os
import tqdm
import server_constants as conts

LOCAL_HOST = conts.LOCAL_HOST #local host

PORT = conts.PORT #port to listen on

BUFFER_SIZE = conts.BUFFER_SIZE #buffer size of data sent and recieved

HEADER = conts.HEADER

TYPE = conts.TYPE

FILE_TYPE = conts.FILE_TYPE

MSG_TYPE = conts.MSG_TYPE




server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((LOCAL_HOST, PORT))
server.listen()

#list of active clients and their nick names
clients = []
nicknames =[]

#contents of the file stored in a list

file_contents = []

def prep_file(filename):
    """
    Open the file and process the data to be sent

    Args:
        filename (string) : name of the file
    """
    filesize = os.path.getsize(filename)
    file_marker = 0
    with open(filename, 'rb') as file_bytes:
        while file_marker <= filesize:
            contents = file_bytes.read(BUFFER_SIZE)
            contents_length = f"{BUFFER_SIZE:<{HEADER}}".encode('utf-8')
            contetns_type = f"{FILE_TYPE:<{TYPE}}".encode('utf-8')
            package = contetns_type + contents_length + contents
            file_contents.append(package)
            file_marker += BUFFER_SIZE
               


def send_file(filename, client):
    """
    Send a file to the client

    Args:
        filename (string) : Name of the file
        client (socket) : An instance of socket
    """
    prep_file(filename)
    filesize = os.path.getsize(filename)
    progress = tqdm.tqdm(range(filesize),f"Sending {filename}", unit='B', unit_scale=True,
            unit_divisor=BUFFER_SIZE, miniters=1, smoothing=1)
    for contents in file_contents:
        client.send(contents)
        progress.update(BUFFER_SIZE)
        progress.refresh()
    message = prep_message("SUCCESS", conts.FILE_COMPLETION_TYPE)
    client.send(message)


def prep_message(message, type):
    """
    Prep the message to be sent by adding the header to the message

    The header will tell the user how long the message is

    Args:
        message (string) : Message to be preped
    
    """
    message = message.encode('utf-8')

    message_length = len(message)

    message_header = (f"{message_length:<{HEADER}}").encode("utf-8")

    message_type = (f"{type:<{TYPE}}").encode("utf-8")

    return message_type + message_header + message



def send_message(message, client):
    """
    Send message to one client.

    Args:
        message (string): message string
        client (socket) : An instance of a socket
    """

    message = prep_message(message, MSG_TYPE)

    client.send(message)



def broadcast(message, origin_client):
    """
    Send message to all clients except the one that orginally wrote the message

    Args:
        message (string): message string
        original_client (socket) : the socket sending the information
    """
    message = prep_message(message, MSG_TYPE)
    for client in clients:
        if client == origin_client:
            pass
        else:
            client.send(message)

def recieve_message(client):
    message_type = client.recv(TYPE).decode('utf-8')
    message_length = int(client.recv(HEADER).decode('utf-8'))
    message = client.recv(message_length).decode('utf-8')
    print(f" Message type: {message_type} Message length: {message_length} Message: {message}")
    return {'type' : message_type, 'length': message_length, 'message' : message}

def broadcast_all(message):
    """
    Sends a message to each client in the server

    Args:
        message (string): the messgae to be sent
    """
    message = prep_message(message, MSG_TYPE)
    for client in clients:
        client.send(message)

def get_nickname(client):
    """
    Get the nickname of the client in question

    Args:
        client (socket) : An instance of a socket
    """
    index = clients.index(client)
    nickname = nicknames[index]
    return nickname

def handle(client):
    """
    handels each client as they come in and dismisses them when they leave

    broacasts messages from clients

    Args:
        client (socket) : client in the server
    
    """
    while True:
        message_dict = recieve_message(client)
        message = message_dict['message']
        check_message = message

        #Get CAT IMAGE
        if check_message == f'{get_nickname(client)}: CAT':
            send_file('cat.jpeg', client)
        else:
            broadcast(message, client)

            



def recieve():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        send_message("NICK", client)
        message_dict = recieve_message(client)
        nickname = message_dict['message']
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}!")
        broadcast(f"{nickname} joined the chat!", client)
        send_message("Connected to the server", client)
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server is listening")
recieve()
        


