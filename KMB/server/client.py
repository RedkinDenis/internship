from codecs import encode
from codecs import decode
from socket import *
import argparse

parser = argparse.ArgumentParser(description='args')
parser.add_argument('--protocol', type=str, default='-t')
parser.add_argument('--ip', type=str, default='127.0.0.1')
args = parser.parse_args()

def UDP_create_socket():
    return socket(AF_INET, SOCK_DGRAM)

def UDP_exchange_message(socket: socket, ip, port, message):
    socket.sendto(encode(message), (ip, port))
    modifiedMessage, serverAddress = socket.recvfrom(2048)
    return modifiedMessage

def TCP_create_socket(ip, port):
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((ip, port))
    return clientSocket

def TCP_exchange_message(socket: socket, ip, port, message):
    clientSocket.send(encode(message))
    modifiedMessage = clientSocket.recv(1024)
    return modifiedMessage




serverPort = 12000
serverName = args.ip

if (args.protocol == '-t'):
    clientSocket = TCP_create_socket(serverName, serverPort)
else:
    clientSocket = UDP_create_socket(serverName, serverPort)

message = input('Input lowercase sentence:')

if (args.protocol == '-t'):
    modifiedMessage = TCP_exchange_message(clientSocket, serverName, serverPort, message)
else:
    modifiedMessage = UDP_exchange_message(clientSocket, serverName, serverPort, message)

print(decode(modifiedMessage))

clientSocket.close()