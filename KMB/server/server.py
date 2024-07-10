from socket import *

def UDP_create_server_socket(port):
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', port))
    return serverSocket

def TCP_create_server_socket(port):
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.bind(('', port))
    serverSocket.listen(1)
    return serverSocket

def TCP_exchange_message(socket: socket, port):
    connectionSocket, addr = socket.accept()
    sentence = connectionSocket.recv(1024)
    capitalizedSentence = sentence.upper()
    connectionSocket.send(capitalizedSentence)
    connectionSocket.close()


def UDP_exchange_message(socket: socket, port):
    message, clientAddress = socket.recvfrom(2048)
    modifiedMessage = message.upper()
    serverSocket.sendto(modifiedMessage, clientAddress)

serverPort = 12000

serverSocket = TCP_create_server_socket(serverPort)

print("The server is ready to receive")

while 1:
    TCP_exchange_message(serverSocket, serverPort)

