import sys
import socket
import pickle
import time
import struct
import subprocess
import threading

class computeNode:
    def __init__(self, size, serverSocket, mat):
        self.size = size / 2
        self.conn , self.addr = serverSocket.accept()
        # sends the size of the submatrix
        data = pickle.dumps(self.size)
        self.conn.sendall(data)

    def sendMat(self, mat):
        # Pickle the matrix
        pickled_data = pickle.dumps(mat)
    
        # Send the size of the pickled data
        size_data = len(pickled_data).to_bytes(4, byteorder='big')
        self.conn.sendall(size_data)
    
        # Send the pickled data
        self.conn.sendall(pickled_data)
    
    def recvMat(self):
        # sends the go command
        go = len(str(self.size)).to_bytes(4, byteorder='big')
        self.conn.sendall(go)

        # Receive the size of the pickled data
        size_data = self.conn.recv(4)  # Assuming the size is sent as a 4-byte integer
        if not size_data:
            return None
        data_size = int.from_bytes(size_data, byteorder='big')
        
        # Receive the pickled data in chunks
        pickled_data = b''
        while len(pickled_data) < data_size:
            chunk = self.conn.recv(min(4096, data_size - len(pickled_data)))
            if not chunk:
                return None
            pickled_data += chunk
        
        # Unpickle the received data
        matrix = pickle.loads(pickled_data)
        return matrix
class CannonController:
    def __init__(self, matAList, matBList, size):
        # makes all the computemode connections
        HOST = '192.168.10.11'
        PORT = 8002
        self.matAlist = matAList
        self.matBlist = matBList
        
        self.computeNodes = []
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind((HOST, PORT))
        serverSocket.listen(4)

        self.socket = serverSocket

        # makes all the node connections
        for i in range(4):
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
        alignedAList.append(self.matAlist[3]) 
        alignedAList.append(self.matAlist[2]) 
        alignedAList.append(self.matAlist[1])
        
        # aligns the B matrix
        alignedBList = []
        alignedBList.append(self.matBlist[0])
        alignedBList.append(self.matBlist[1]) 
        alignedBList.append(self.matBlist[3]) 
        alignedBList.append(self.matBlist[2])

        self.matAlist = alignedAList
        self.matBlist = alignedBList

    def matShift(self):
        # shifts A left 1 and B up 1
        alignedAList = []
        alignedAList.append(self.matAlist[2])
        alignedAList.append(self.matAlist[3]) 
        alignedAList.append(self.matAlist[0]) 
        alignedAList.append(self.matAlist[1])
        
        # aligns the B matrix
        alignedBList = []
        alignedBList.append(self.matBlist[1])
        alignedBList.append(self.matBlist[0]) 
        alignedBList.append(self.matBlist[3]) 
        alignedBList.append(self.matBlist[2])

        self.matAlist = alignedAList
        self.matBlist = alignedBList

    def sendMats(self):
        for i in range(4):
            # sends matrix A and B to each node
            self.computeNodes[i].sendMat(self.matAlist[i])
            self.computeNodes[i].sendMat(self.matBlist[i])

    def recvResultMat(self, index):
        data = self.computeNodes[index].recvMat()
        return data

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
    sub_size = size // 2

    for i in range(0, size, sub_size):
        for j in range(0, size, sub_size):
            submatrix = [matrix[x][j:j+sub_size] for x in range(i, i+sub_size)]
            submatrices.append(submatrix)

    return submatrices

def combine_submatrices(submatrices):
    submatrix_size = len(submatrices[0])
    matrix_size = submatrix_size * 2
    combined_matrix = [[0] * matrix_size for _ in range(matrix_size)]

    for i, submatrix in enumerate(submatrices):
        row_start = (i // 2) * submatrix_size
        col_start = (i % 2) * submatrix_size

        for row_offset, row in enumerate(submatrix):
            for col_offset, value in enumerate(row):
                combined_matrix[row_start + row_offset][col_start + col_offset] = value

    return combined_matrix

def write_matrix_to_binary_file(matrix, filename):
    with open(filename, 'wb') as file:
        # Write the number of rows and columns as the first line
        rows = len(matrix)
        cols = len(matrix[0])
        file.write(struct.pack('ii', rows, cols))

        # Write each element of the matrix to the file
        for row in matrix:
            for element in row:
                file.write(struct.pack('i', element))

def iperfThread():
    iperf_command = ['iperf', '-c', '192.168.10.11', '-p', '8002']
    iperf_process = subprocess.Popen(iperf_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in iperf_process.stdout:
        print(line.strip())


def main():
    # gets the 2 matrices from the files into memory 
    (matA, size) = read_matrix_from_binary("matA.bin")
    (matB, size) = read_matrix_from_binary("matB.bin")
    
    matASubs = split_matrix(matA, size)
    matBSubs = split_matrix(matB, size)
    

    controller = CannonController(matAList=matASubs, matBList=matBSubs, size=size)

    iperf_thread = threading.Thread(target=iperfThread)
    iperf_thread.start()
    # does the shifting and sending of the matrices
    start = time.time()
    for i in range(2):
        controller.sendMats()
        controller.matShift()
    # recives the result mats
    results = []
    for i in range(4):
        submat = controller.recvResultMat(i)
        results.append(submat)
    # puts the matrix back together
    wholeMat = combine_submatrices(results)
    end = time.time()
    runtime = end - start
    
    controller.socket.close()
    iperf_thread.join()
    print("time to fininsh = ", runtime, "\n")
    write_matrix_to_binary_file(matrix=wholeMat, filename="parallelResult.bin")

main()
    
    
    
