from codecs import encode
from codecs import decode
from socket import *

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

serverName = '127.0.0.1'
serverPort = 12000

clientSocket = TCP_create_socket(serverName, serverPort)
message = input('Input lowercase sentence:')
modifiedMessage = TCP_exchange_message(clientSocket, serverName, serverPort, message)

print(decode(modifiedMessage))

clientSocket.close()