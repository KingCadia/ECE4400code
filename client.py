import sys
import socket
import pickle
import struct

def main():
    # sets up socket
    HOST = '192.168.10.11'  
    PORT = 12345
    nodeSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connects to the server
    nodeSocket.connect((HOST, PORT))
    size = nodeSocket.recv(4)
    received_int = struct.unpack('!i', size)[0]
    print(received_int)
main()