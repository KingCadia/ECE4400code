import sys
import socket
import pickle

def addMatrix(matA, matB, result):
    for i in range(len(matA)):
        for j in range(len(matA[0])):
            result[i][j] += matA[i][j] + matB[i][j]
    return result

def main():
    # sets up socket
    HOST = '192.168.10.11'  
    PORT = 1234
    nodeSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connects to the server and gets the size of the matrix
    nodeSocket.connect((HOST, PORT))
    size = nodeSocket.recv(4)
    
    size = pickle.loads(size)
    nodeSocket.send(pickle.dumps(1024))
    bufferSize = int(pickle.loads(nodeSocket.recv(4)))
    nodeSocket.send(pickle.dumps(1024))

    size = int(size)
    # intalizes the result matrix
    result = [[0] * size] * size

    for i in range(2):
        # recevies the a and b matrices
        matA = pickle.loads(nodeSocket.recv(bufferSize))
        nodeSocket.send(pickle.dumps(1))
        matB = pickle.loads(nodeSocket.recv(bufferSize))
        nodeSocket.send(pickle.dumps(1))
        result = addMatrix(matA=matA, matB=matB, result=result)

    # sends the result matrix back

    # waits for nodes turn to transmit
    go = nodeSocket.recv(4096)
    nodeSocket.send(pickle.dumps(result))
    
main()