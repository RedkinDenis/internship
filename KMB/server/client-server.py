from codecs import encode
from codecs import decode
from socket import *
import argparse



parser = argparse.ArgumentParser(description='args')
parser.add_argument('--mode', type=str, choices={'-s', '-c'}, default='none')
parser.add_argument('--protocol', type=str, default='-t')
parser.add_argument('--ip', type=str, default='127.0.0.1')
parser.add_argument('-f', type=str, default='none')
args = parser.parse_args()



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
    serverSocket.sendto(clientAddress, clientAddress)

serverPort = 12000

# client

if (args.mode == '-c'):
    
    if (args.f != 'none'):
        log_file = open(args.f + '.txt', 'w')
    else:
        log_file = 0

    log = lambda str: print(str) if args.f == 'none' else log_file.write(str)

    serverName = args.ip

    if (args.protocol == '-t'):
        log('protocol - TCP ')
        clientSocket = client_TCP_create_socket(serverName, serverPort)
    else:
        log('protocol - UDP ')
        clientSocket = client_UDP_create_socket(serverName, serverPort)

    log('server adress - ' + args.ip + ', port - ' + str(serverPort) + '\n')

    log('socket has been created\n')

    if (args.protocol == '-t'):
        modifiedMessage = client_TCP_exchange_message(clientSocket, serverName, serverPort, log_file)
    else:
        modifiedMessage = client_UDP_exchange_message(clientSocket, serverName, serverPort, log_file)

    log('result - ' + decode(modifiedMessage))

    clientSocket.close()

    log('\nsocket has been closed')


# server

if (args.mode == '-s'):

    if (args.protocol == '-t'):
        serverSocket = server_TCP_create_server_socket(serverPort)
    else:
        serverSocket = server_UDP_create_server_socket(serverPort)

    print('The server is ready to receive')

    while 1:
        if (args.protocol == '-t'):
            server_TCP_exchange_message(serverSocket, serverPort)
        else:
            server_UDP_exchange_message(serverSocket, serverPort)