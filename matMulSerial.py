import struct
import time

def read_matrix_from_binary_file(filename):
    with open(filename, 'rb') as file:
        # Read the number of rows and columns
        rows, cols = struct.unpack('ii', file.read(8))
        matrix = []

        # Read the elements of the matrix
        for _ in range(rows):
            row = struct.unpack('i' * cols, file.read(4 * cols))
            matrix.append(row)

        return matrix

def write_matrix_to_binary_file(matrix, filename):
    with open(filename, 'wb') as file:
        # Write the number of rows and columns
        rows = len(matrix)
        cols = len(matrix[0])
        file.write(struct.pack('ii', rows, cols))

        # Write each element of the matrix
        for row in matrix:
            for element in row:
                file.write(struct.pack('i', element))

def multiply_matrices(matrix_a, matrix_b):
    result = []
    for i in range(len(matrix_a)):
        row = []
        for j in range(len(matrix_b[0])):
            element_sum = 0
            for k in range(len(matrix_b)):
                element_sum += matrix_a[i][k] * matrix_b[k][j]
            row.append(element_sum)
        result.append(row)
    return result

# Read matrices from files
matA = read_matrix_from_binary_file("matA.bin")
matB = read_matrix_from_binary_file("matB.bin")

start = time.time()
# Perform matrix multiplication
result = multiply_matrices(matA, matB)
end = time.time()
runtime = end - start
print("time to fininsh = ", runtime, "\n")
# Write the result to serialResult.bin
write_matrix_to_binary_file(result, "serialResult.bin")