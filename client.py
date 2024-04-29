import sys
import socket
import pickle
import struct

def addMatrix(matA, matB, result):
    for i in range(len(matA)):
        for j in range(len(matA[0])):
            result[i][j] += matA[i][j] + matB[i][j]
    return result

def main():
    # sets up socket
    HOST = '192.168.10.11'  
    PORT = 12345
    nodeSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connects to the server and gets the size of the matrix
    nodeSocket.connect((HOST, PORT))
    size = nodeSocket.recv(4096)
    size = pickle.loads(size)

    size = int(size)
    # intalizes the result matrix
    result = [[0] * size] * size

    for i in range(1):
        # recevies the a and b matrices
        matA = nodeSocket.recv(sys.getsizeof(result))
        matB = nodeSocket.recv(sys.getsizeof(result))

    print(matA)
main()