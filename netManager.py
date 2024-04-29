import sys
import socket
import pickle
import subprocess
import threading
import time
import struct

class computeNode:
    def __init__(self, size, serverSocket, mat):
        self.size = size / 3
        self.conn , self.addr = serverSocket.accept()
        # sends the size of the submatrix
        data = pickle.dumps(self.size)
        self.conn.send(data)
        data = pickle.dumps(mat)
        self.size = sys.getsizeof(data)

    def sendMat(self, mat):
        self.conn.send(pickle.dumps(mat))
    
    def recvMat(self):
        data = self.conn.recv(self.size)
        data = pickle.loads(data)
        return data


class CannonController:
    def __init__(self, matAList, matBList, size):
        # makes all the computemode connections
        HOST = '192.168.10.11'
        PORT = 12345
        self.matAlist = matAList
        self.matBlist = matBList
        
        self.computeNodes = []
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind((HOST, PORT))
        serverSocket.listen(9)

        # makes all the node connections
        for i in range(1):
            node = computeNode(size=size, serverSocket=serverSocket, mat=matAList[0])
            self.computeNodes.append(node)
        
        # aligns the matrices
        self.matAlist = matAList
        self.matBlist = matBList
        self.matSize = size
        self.matrixalign()

    def matrixalign(self):
        # does the inital alignment of the 2 matrices
        
        # aligns the A matrix
        alignedAList = []
        alignedAList.append(self.matAlist[0])
        alignedAList.append(self.matAlist[1]) 
        alignedAList.append(self.matAlist[2]) 
        alignedAList.append(self.matAlist[4])
        alignedAList.append(self.matAlist[5])
        alignedAList.append(self.matAlist[3])
        alignedAList.append(self.matAlist[8])
        alignedAList.append(self.matAlist[6]) 
        alignedAList.append(self.matAlist[7])

        # aligns the B matrix
        alignedBList = []
        alignedBList.append(self.matBlist[0])
        alignedBList.append(self.matBlist[4]) 
        alignedBList.append(self.matBlist[8]) 
        alignedBList.append(self.matBlist[3])
        alignedBList.append(self.matBlist[7])
        alignedBList.append(self.matBlist[2])
        alignedBList.append(self.matBlist[6])
        alignedBList.append(self.matBlist[1]) 
        alignedBList.append(self.matBlist[5])

        self.matAlist = alignedAList
        self.matBlist = alignedBList

    def matShift(self):
        # shifts A left 1 and B up 1
        alignedAList = []
        alignedAList.append(self.matAlist[1])
        alignedAList.append(self.matAlist[2]) 
        alignedAList.append(self.matAlist[0]) 
        alignedAList.append(self.matAlist[4])
        alignedAList.append(self.matAlist[5])
        alignedAList.append(self.matAlist[3])
        alignedAList.append(self.matAlist[7])
        alignedAList.append(self.matAlist[8]) 
        alignedAList.append(self.matAlist[6])

        # aligns the B matrix
        alignedBList = []
        alignedBList.append(self.matBlist[3])
        alignedBList.append(self.matBlist[4]) 
        alignedBList.append(self.matBlist[5]) 
        alignedBList.append(self.matBlist[6])
        alignedBList.append(self.matBlist[7])
        alignedBList.append(self.matBlist[8])
        alignedBList.append(self.matBlist[0])
        alignedBList.append(self.matBlist[1]) 
        alignedBList.append(self.matBlist[2])

        self.matAlist = alignedAList
        self.matBlist = alignedBList

    def sendMats(self):
        for i in range(1):
            # sends matrix A and B to each node
            self.computeNodes[i].sendMat(self.matAlist[i])
            self.computeNodes[i].sendMat(self.matBlist[i])

    def recvResultMat(self, index):
        data = self.computeNodes[index].recvMat()

# function to read a matrix into memory
def read_matrix_from_binary(file_path):
    try:
        # Open the binary file in binary read mode
        with open(file_path, "rb") as file:
            # Read the size of the matrix (2 integers)
            size_bytes = file.read(8)  # 2 integers, each of size 4 bytes
            # Unpack the size from bytes to integers
            size = struct.unpack('ii', size_bytes)

            # Initialize an empty matrix of the specified size
            matrix = [[0.0 for _ in range(size[1])] for _ in range(size[0])]

            # Read each float value from the binary file and populate the matrix
            for i in range(size[0]):
                for j in range(size[1]):
                    # Read a float value (4 bytes) from the file
                    int_bytes = file.read(4)
                    # Convert the bytes to a float using the 'f' format of struct.unpack
                    matrix[i][j] = struct.unpack('i', int_bytes)[0]
    except FileNotFoundError:
        print("File not found.")
        return None
    except Exception as e:
        print("An error occurred:", e)
        return None

    return matrix, size[1]

# function to split the matrix into equal parts
def split_matrix(matrix, size):
    submatrices = []
    sub_size = size // 3

    for i in range(0, size, sub_size):
        for j in range(0, size, sub_size):
            submatrix = [matrix[x][j:j+sub_size] for x in range(i, i+sub_size)]
            submatrices.append(submatrix)

    return submatrices

def main():
    # gets the 2 matrices from the files into memory 
    (matA, size) = read_matrix_from_binary("matA.bin")
    (matB, size) = read_matrix_from_binary("matB.bin")
    
    matASubs = split_matrix(matA, size)
    matBSubs = split_matrix(matB, size)
    
    controller = CannonController(matAList=matASubs, matBList=matBSubs, size=size)

    # does the shifting and sending of the matrices 
    for i in range(1):
        controller.sendMats()
        controller.matShift()

    # recives the result mats
    results = []
    for i in range(1):
        submat = controller.recvResultMat(i)
    
main()
    
    