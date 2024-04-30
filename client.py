import sys
import socket
import pickle

def sendMat(self, mat, conn):
        # Pickle the matrix
        pickled_data = pickle.dumps(mat)
    
        # Send the size of the pickled data
        size_data = len(pickled_data).to_bytes(4, byteorder='big')
        conn.sendall(size_data)
    
        # Send the pickled data
        conn.sendall(pickled_data)

def receive_matrix(sock):
    # Receive the size of the pickled data
    size_data = sock.recv(4)  # Assuming the size is sent as a 4-byte integer
    if not size_data:
        return None
    data_size = int.from_bytes(size_data, byteorder='big')
    
    # Receive the pickled data in chunks
    pickled_data = b''
    while len(pickled_data) < data_size:
        chunk = sock.recv(min(4096, data_size - len(pickled_data)))
        if not chunk:
            return None
        pickled_data += chunk
    
    # Unpickle the received data
    matrix = pickle.loads(pickled_data)
    return matrix


def addMatrix(matA, matB, result):
    for i in range(len(matA)):
        for j in range(len(matA[0])):
            result[i][j] += matA[i][j] + matB[i][j]
    return result

def main():
    # sets up socket
    HOST = '192.168.10.11'  
    PORT = 12376
    nodeSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connects to the server and gets the size of the matrix
    nodeSocket.connect((HOST, PORT))
    size = nodeSocket.recv(4096)
    
    size = pickle.loads(size)

    size = int(size)
    # intalizes the result matrix
    result = [[0] * size] * size

    for i in range(2):
        # recevies the a and b matrices
        matA = receive_matrix(nodeSocket)

        matB = receive_matrix(nodeSocket)

        result = addMatrix(matA=matA, matB=matB, result=result)

    # sends the result matrix back

    # waits for nodes turn to transmit
    go = nodeSocket.recv(4096)
    sendMat(mat=result, conn=nodeSocket)
    
main()