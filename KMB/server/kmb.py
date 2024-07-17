from codecs import encode
from codecs import decode
import socket as sk
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='args')
    parser.add_argument('ip', type=str, help='enter adress')  #loop='127.0.0.1'
    parser.add_argument('p', type=int, help='enter number of port')

    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('-s', action='store_true', help='if you want to use server mode')
    mode.add_argument('-c', action='store_true', help='client mode')
    
    protocol = parser.add_mutually_exclusive_group()
    protocol.add_argument('-t', action='store_true', help='if you want to use TCP protocol')
    protocol.add_argument('-u', action='store_true', help='UDP protocol')
    
    parser.add_argument('-f', type=str, default='none', help='if you want to write logs to file')
    args = parser.parse_args()

    return args

def client_UDP_create_socket():
    # print(1)
    return sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

def client_TCP_create_socket(ip, port):
    # print(2)
    clientSocket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    clientSocket.connect((ip, port))
    return clientSocket

def client_UDP_exchange_message(socket: sk.socket, ip, port, log_file):  
    socket.sendto(encode('message'), (ip, port))
    log('The message has been sent\n')
    modifiedMessage, _ = socket.recvfrom(2048)
    log('The message has been received\n')
    return modifiedMessage

def client_TCP_exchange_message(socket: sk.socket, ip, port, log_file):
    modifiedMessage = socket.recv(1024)
    log('The message has been received\n')
    return modifiedMessage

def server_UDP_create_server_socket(addres, port):
    serverSocket = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    serverSocket.bind((addres, port))
    return serverSocket

def server_TCP_create_server_socket(addres, port):
    serverSocket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    serverSocket.bind((addres, port))
    serverSocket.listen(1)
    return serverSocket

def server_TCP_exchange_message(socket: sk.socket, port):
    connectionSocket, addr = socket.accept()
    connectionSocket.send(encode(addr[0] + ' ' + str(addr[1])))
    connectionSocket.close()

def server_UDP_exchange_message(socket: sk.socket, port):
    _, clientAddress = socket.recvfrom(2048)
    socket.sendto(encode(clientAddress[0] + ' ' + str(clientAddress[1])), clientAddress)

def client_TCP(serverName, serverPort):
    log('protocol - TCP ')
    clientSocket = client_TCP_create_socket(serverName, serverPort)
    
    log('server adress - ' + serverName + ', port - ' + str(serverPort) + '\n')

    log('socket has been created\n')

    modifiedMessage = client_TCP_exchange_message(clientSocket, serverName, serverPort, log_file)
   
    log('result - ' + decode(modifiedMessage))

    clientSocket.close()

    log('\nsocket has been closed')

def client_UDP(serverName, serverPort):
    log('protocol - UDP ')
    clientSocket = client_UDP_create_socket()

    log('server adress - ' + serverName + ', port - ' + str(serverPort) + '\n')

    log('socket has been created\n')

    modifiedMessage = client_UDP_exchange_message(clientSocket, serverName, serverPort, log_file)

    log('result - ' + decode(modifiedMessage))

    clientSocket.close()

    log('\nsocket has been closed')

def server_TCP(serverName, serverPort):
    serverSocket = server_TCP_create_server_socket(serverName, serverPort)

    print('The server is ready to receive')

    while 1:
        server_TCP_exchange_message(serverSocket, serverPort)

def server_UDP(serverName, serverPort):
    serverSocket = server_UDP_create_server_socket(serverName, serverPort)

    print('The server is ready to receive')

    while 1:
        server_UDP_exchange_message(serverSocket, serverPort)

def mask(s, c, t, u):
    res = str(int(s)) + str(int(c)) + str(int(t)) + str(int(u))
    return res


# if __name__ == '__main__':
#     main()

args = parse_args()
serverPort = args.p
serverName = args.ip

if (args.f != 'none'):
    log_file = open(args.f + '.txt', 'w')
else:
    log_file = 0
log = lambda str: print(str) if args.f == 'none' else log_file.write(str)

mode = {'1010':server_TCP, '1001':server_UDP, '0110': client_TCP, '0101':client_UDP}

mode[mask(args.s, args.c, args.t, args.u)](serverName, serverPort)

