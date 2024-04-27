def break_into_submatrices(matrix, size):
    submatrices = []
    sub_size = size // 3

    for i in range(0, size, sub_size):
        for j in range(0, size, sub_size):
            submatrix = [matrix[x][j:j+sub_size] for x in range(i, i+sub_size)]
            submatrices.append(submatrix)

    return submatrices

# Example usage:
matrix = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 5, 6, 7, 8, 9]
]
submatrices = break_into_submatrices(matrix, 9)
for submatrix in submatrices:
    print(submatrix)