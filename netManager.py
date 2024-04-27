import sys
import socket
import pickle
import subprocess
import threading
import time
import struct

portNum = 2525

class computeNode:
    def __init__(self, size):
        hostName = socket.gethostname()
        # creates socket object
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((hostName, portNum))
        portNum = portNum + 1
        self.socket.listen(9)
        
        # gets a connection from one of the compute nodes
        self.conn, self.addr = self.socket.accept()
        
        # sends the size of the matrix
        dataString = pickle.dumps(size)
        self.conn.sendall(dataString)
        self.size = size

    def sendMat(self, subMat):
        data = pickle.dumps(subMat)
        self.conn.send(data)

    def recvMat(self):
        mat = self.conn.recv(self.size * self.size * 32)
        return mat

class CannonController:
    def __init__(self, matAList, matBList, size):
        # makes all the computemode connections
        self.computeNodes = []
        for i in range(8):
            node = computeNode()
            self.computeNodes.append(node)
            self.matAlist = matAList
            self.matBlist = matBList
            self.matSize = size
        # aligns the matrices
        self.matrixalign()


    def matrixalign(self):
        # does the inital alignment of the 2 matrices
        
        # aligns the A matrix
        alignedAList = []
        alignedAList[0] = self.matAlist[0]
        alignedAList[1] = self.matAlist[1]
        alignedAList[2] = self.matAlist[2]
        alignedAList[3] = self.matAlist[4]
        alignedAList[4] = self.matAlist[5]
        alignedAList[5] = self.matAlist[3]
        alignedAList[6] = self.matAlist[8]
        alignedAList[7] = self.matAlist[6]
        alignedAList[8] = self.matAlist[7]

        # aligns the B matrix
        alignedBList = []
        alignedBList[0] = self.matBlist[0]
        alignedBList[1] = self.matBlist[4]
        alignedBList[2] = self.matBlist[8]
        alignedBList[3] = self.matBlist[3]
        alignedBList[4] = self.matBlist[7]
        alignedBList[5] = self.matBlist[2]
        alignedBList[6] = self.matBlist[6]
        alignedBList[7] = self.matBlist[1]
        alignedBList[8] = self.matBlist[5]

        self.matAlist = alignedAList
        self.matBlist = alignedBList

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
                    float_bytes = file.read(4)
                    # Convert the bytes to a float using the 'f' format of struct.unpack
                    matrix[i][j] = struct.unpack('f', float_bytes)[0]
    except FileNotFoundError:
        print("File not found.")
        return None
    except Exception as e:
        print("An error occurred:", e)
        return None

    return matrix, size[0]

# function to split the matrix into equal parts
def split_matrix(matrix):
    submatrices = []

    # Calculate the dimensions of each submatrix
    submatrix_rows = len(matrix) // 3
    submatrix_cols = len(matrix[0]) // 3

    # Iterate through the original matrix and extract submatrices
    for i in range(3):
        for j in range(3):
            # Initialize an empty submatrix
            submatrix = [[0.0 for _ in range(submatrix_cols)] for _ in range(submatrix_rows)]
            # Copy values from the original matrix to the submatrix
            for m in range(submatrix_rows):
                for n in range(submatrix_cols):
                    submatrix[m][n] = matrix[i * submatrix_rows + m][j * submatrix_cols + n]
            # Append the submatrix to the list
            submatrices.append(submatrix)

    return submatrices

def main():
    # gets the 2 matrices from the files into memory 
    matA, size = read_matrix_from_binary("matA.bin")
    matB, size = read_matrix_from_binary("matB.bin")
    
    matASubs = split_matrix(matA)
    matBSubs = split_matrix(matB)
    
    controller = CannonController(matAList=matASubs, matBList=matBSubs, size=size)
    
    
    
    