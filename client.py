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
    PORT = 12345
    nodeSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connects to the server and gets the size of the matrix
    nodeSocket.connect((HOST, PORT))
    size = nodeSocket.recv(4096)
    size = pickle.loads(size)

    size = int(size)
    # intalizes the result matrix
    result = [[0] * size] * size

    for i in range(3):
        # recevies the a and b matrices
        matA = nodeSocket.recv(sys.getsizeof(result))
        matA = pickle.loads(matA)
        matB = nodeSocket.recv(sys.getsizeof(result))
        matB = pickle.loads(matB)
        result = addMatrix(matA=matA, matB=matB, result=result)

    # sends the result matrix back

    # waits for nodes turn to transmit
    go = nodeSocket.recv(4096)
    nodeSocket.send(pickle.dumps(result))
    
main()