from codecs import encode
from codecs import decode
from socket import *

serverName = '127.0.0.1'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

message = input('Input lowercase sentence:')
# message = b'abcd'

clientSocket.sendto(encode(message),(serverName,serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

print(decode(modifiedMessage))

clientSocket.close()



