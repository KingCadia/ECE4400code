import sys
import socket
import pickle

def main():
    # sets up socket
    HOST = '192.168.10.0'  
    PORT = 12345
    nodeSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connects to the server
    size = nodeSocket.recv(4)
    size = pickle.loads(size)

    print(size)
main()