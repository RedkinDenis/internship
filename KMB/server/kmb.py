from codecs import encode
from codecs import decode
from socket import *
import argparse



parser = argparse.ArgumentParser(description='args')
parser.add_argument('ip', type=str)  #loop='127.0.0.1'
parser.add_argument('p', type=int)
parser.add_argument('-s', action='store_true')
parser.add_argument('-c', action='store_true')
parser.add_argument('-t', action='store_true')
parser.add_argument('-u', action='store_true')
parser.add_argument('-f', type=str, default='none')
args = parser.parse_args()

if ((args.s == args.c == True) or (args.u == args.t == True)):
    exit

def client_UDP_create_socket():
    return socket(AF_INET, SOCK_DGRAM)

def client_TCP_create_socket(ip, port):
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((ip, port))
    return clientSocket

def client_UDP_exchange_message(socket: socket, ip, port, log_file):  
    socket.sendto(encode('message'), (ip, port))
    log('The message has been sent\n')
    modifiedMessage, serverAddress = socket.recvfrom(2048)
    log('The message has been received\n')
    return modifiedMessage

def client_TCP_exchange_message(socket: socket, ip, port, log_file):
    modifiedMessage = clientSocket.recv(1024)
    log('The message has been received\n')
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
    connectionSocket.send(encode(addr[0] + ' ' + str(addr[1])))
    connectionSocket.close()

def server_UDP_exchange_message(socket: socket, port):
    message, clientAddress = socket.recvfrom(2048)
    serverSocket.sendto(encode(clientAddress[0] + ' ' + str(clientAddress[1])), clientAddress)


serverPort = args.p

# client

if (args.c == True):
    
    if (args.f != 'none'):
        log_file = open(args.f + '.txt', 'w')
    else:
        log_file = 0

    log = lambda str: print(str) if args.f == 'none' else log_file.write(str)

    serverName = args.ip

    if (args.u == False):
        log('protocol - TCP ')
        clientSocket = client_TCP_create_socket(serverName, serverPort)
    else:
        log('protocol - UDP ')
        clientSocket = client_UDP_create_socket()

    log('server adress - ' + args.ip + ', port - ' + str(serverPort) + '\n')

    log('socket has been created\n')

    if (args.u == False):
        modifiedMessage = client_TCP_exchange_message(clientSocket, serverName, serverPort, log_file)
    else:
        modifiedMessage = client_UDP_exchange_message(clientSocket, serverName, serverPort, log_file)

    log('result - ' + decode(modifiedMessage))

    clientSocket.close()

    log('\nsocket has been closed')


# server

if (args.s == True):

    if (args.u == False):
        serverSocket = server_TCP_create_server_socket(serverPort)
    else:
        serverSocket = server_UDP_create_server_socket(serverPort)

    print('The server is ready to receive')

    while 1:
        if (args.u == False):
            server_TCP_exchange_message(serverSocket, serverPort)
        else:
            server_UDP_exchange_message(serverSocket, serverPort)