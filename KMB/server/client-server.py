from codecs import encode
from codecs import decode
from socket import *
import argparse



parser = argparse.ArgumentParser(description='args')
parser.add_argument('--mode', type=str, choices={'-s', '-c'}, default='none')
parser.add_argument('--protocol', type=str, default='-t')
parser.add_argument('--ip', type=str, default='127.0.0.1')
args = parser.parse_args()



def client_UDP_create_socket():
    return socket(AF_INET, SOCK_DGRAM)

def client_UDP_exchange_message(socket: socket, ip, port, message):
    socket.sendto(encode(message), (ip, port))
    modifiedMessage, serverAddress = socket.recvfrom(2048)
    return modifiedMessage

def client_TCP_create_socket(ip, port):
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((ip, port))
    return clientSocket

def client_TCP_exchange_message(socket: socket, ip, port, message):
    clientSocket.send(encode(message))
    modifiedMessage = clientSocket.recv(1024)
    return modifiedMessage



def server_UDP_create_server_socket(port):
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', port))
    return serverSocket

def server_TCP_create_server_socket(port):
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.bind(('', port))
    serverSocket.listen(1)
    return serverSocket

def server_TCP_exchange_message(socket: socket, port):
    connectionSocket, addr = socket.accept()
    sentence = connectionSocket.recv(1024)
    capitalizedSentence = sentence.upper()
    connectionSocket.send(capitalizedSentence)
    connectionSocket.close()

def server_UDP_exchange_message(socket: socket, port):
    message, clientAddress = socket.recvfrom(2048)
    modifiedMessage = message.upper()
    serverSocket.sendto(modifiedMessage, clientAddress)



serverPort = 12000

# client

if (args.mode == '-c'):

    serverName = args.ip

    if (args.protocol == '-t'):
        clientSocket = client_TCP_create_socket(serverName, serverPort)
    else:
        clientSocket = client_UDP_create_socket(serverName, serverPort)

    message = input('Input lowercase sentence:')

    if (args.protocol == '-t'):
        modifiedMessage = client_TCP_exchange_message(clientSocket, serverName, serverPort, message)
    else:
        modifiedMessage = client_UDP_exchange_message(clientSocket, serverName, serverPort, message)

    print(decode(modifiedMessage))

    clientSocket.close()



# server

if (args.mode == '-s'):

    if (args.protocol == '-t'):
        serverSocket = server_TCP_create_server_socket(serverPort)
    else:
        serverSocket = server_UDP_create_server_socket(serverPort)

    print("The server is ready to receive")

    while 1:
        if (args.protocol == '-t'):
            server_TCP_exchange_message(serverSocket, serverPort)
        else:
            server_UDP_exchange_message(serverSocket, serverPort)