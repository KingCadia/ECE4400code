import sys
import random
import struct

def generate_random_matrix(size):
    matrix = [[random.randint(0, 100) for _ in range(size)] for _ in range(size)]
    return matrix

def write_matrix_to_file(matrix, filename):
    with open(filename, 'wb') as f:
        # Write the size of the matrix as the first two numbers in the file
        f.write(struct.pack('ii', len(matrix), len(matrix[0])))
        
        # Write the matrix to the file
        for row in matrix:
            f.write(struct.pack('i' * len(row), *row))

matrix_size = int(sys.argv[1])
output_filename = sys.argv[2] 
# Generate random square matrix
matrix = generate_random_matrix(matrix_size)

# Write matrix to file
write_matrix_to_file(matrix, output_filename)