import socket

import threading
import tqdm
import time
import server_constants as conts

LOCAL_HOST = conts.LOCAL_HOST #local host

PORT = conts.PORT #port to listen on

BUFFER_SIZE = conts.BUFFER_SIZE #buffer size of data sent and recieved

HEADER = conts.HEADER

TYPE = conts.TYPE

FILE_TYPE = conts.FILE_TYPE

MSG_TYPE = conts.MSG_TYPE

file_contents = []

nickname = input("Name: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((LOCAL_HOST, PORT))

file_flag = False

filesize = 0

def recieve_file(filename):
    """
    Open a new file and loop through it until the file is
    completely written

    Args:
        filename (string) : Name of the new file
    """
    with open(filename, 'wb') as f:
        for contents in file_contents:
            f.write(contents)
    print(f"\nFile recieved\nFile saved as {filename}\n")
    

def prep_message(message):
    """
    Prep the message to be sent by adding the header to the message

    The header will tell the user how long the message is

    Args:
        message (string) : Message to be preped
    
    """
    message = message.encode('utf-8')

    message_length = len(message)

    message_header = (f"{message_length:<{HEADER}}").encode("utf-8")

    message_type = (f"{MSG_TYPE:<{TYPE}}").encode("utf-8")

    return message_type + message_header + message

def send_message(message):
    """
    Send message to one client.

    Args:
        message (string): message string
        client (socket) : An instance of a socket
    """

    message = prep_message(message)

    client.send(message)


def recieve_message():
    """
    Recieve and decode the message from the server
    """
    message_type = client.recv(TYPE).decode('utf-8')
    message_length = int(client.recv(HEADER).decode('utf-8'))
    # print(f" message type: {message_type} message_length: {message_length}")
    if message_type.strip() == FILE_TYPE:
        message = client.recv(message_length)
    else:
        message = client.recv(message_length).decode('utf-8')
    return {'type' : message_type, 'length': message_length, 'message' : message}


def receive():
    """
    Thread that runs connection to the server and
    Recieve and process data from the server
    """
    
    while True:

        message_dict = recieve_message()
        message = message_dict['message']
        message_type = message_dict['type']

        if message_type.strip() == FILE_TYPE:
            file_contents.append(message)
            
        elif message_type.strip() == MSG_TYPE:
            if message == 'NICK':
                send_message(nickname)
                # client.send(nickname.encode('utf-8'))
            else:
                print(message)
        elif message_type.strip() == conts.FILE_COMPLETION_TYPE:
            recieve_file('new_file.jpeg')
        else:
            print("The sent message is of unknown type")
            print()
            print("Please contact an administrator\n")

def write():
    """
    Thread that runs input to the server
    """
    while True:
        message = f'{nickname}: {input("")}'
        send_message(message)


receive_thread = threading.Thread(target=receive)
write_thread = threading.Thread(target=write)


receive_thread.start()
write_thread.start()

