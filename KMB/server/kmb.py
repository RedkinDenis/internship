from codecs import encode
from codecs import decode
import socket as sk
import argparse
import logging

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
    
    log = parser.add_mutually_exclusive_group()
    log.add_argument('-o', action='store_true', help='stdout')
    log.add_argument('-f', type=str, default='none', help='if you want to write logs to file')
    args = parser.parse_args()

    return args

def client_UDP_create_socket(serverName, serverPort):
    socket = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    logger.info('server adress - ' + serverName + ', port - ' + str(serverPort) + '')
    logger.info('socket has been created')
    return socket

def client_TCP_create_socket(ip, port):
    clientSocket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    clientSocket.connect((ip, port))
    logger.info('server adress - ' + ip + ', port - ' + str(port) + '')
    logger.info('socket has been created')
    return clientSocket

def client_UDP_exchange_message(socket: sk.socket, ip, port):  
    socket.sendto(encode('message'), (ip, port))
    logger.info('The message has been sent')
    modifiedMessage, _ = socket.recvfrom(2048)
    logger.info('The message has been received')
    return modifiedMessage

def client_TCP_exchange_message(socket: sk.socket, ip, port):
    modifiedMessage = socket.recv(1024)
    logger.info('The message has been received')
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
    logger.info('protocol - TCP ')
    clientSocket = client_TCP_create_socket(serverName, serverPort)

    modifiedMessage = client_TCP_exchange_message(clientSocket, serverName, serverPort)
   
    logger.info('result - ' + decode(modifiedMessage))

    clientSocket.close()

    logger.info('socket has been closed')

def client_UDP(serverName, serverPort):
    logger.info('protocol - UDP ')
    clientSocket = client_UDP_create_socket(logger)

    modifiedMessage = client_UDP_exchange_message(clientSocket, serverName, serverPort)

    logger.info('result - ' + decode(modifiedMessage))

    clientSocket.close()

    logger.info('socket has been closed')

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
    res = int(u) + 2 * int(t) + 4 * int(c) + 8 * int(s)
    return res

def main():
    args = parse_args()
    serverPort = args.p
    serverName = args.ip

    mode = {0b1010:server_TCP, 0b1001:server_UDP, 0b0110: client_TCP, 0b0101:client_UDP}

    global logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    if (args.f != 'none'):
        handler = logging.FileHandler(f"{args.f}.log", mode='w')
    elif (args.o == True):
        handler = logging.StreamHandler()
    else:
        handler = logging.StreamHandler()    

    formatter = logging.Formatter("%(funcName)s %(asctime)s %(levelname)s %(message)s")
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    mode[mask(args.s, args.c, args.t, args.u)](serverName, serverPort)


if __name__ == '__main__':
    main()