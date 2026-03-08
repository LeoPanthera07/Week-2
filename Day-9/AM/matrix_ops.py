def matrix_add(A, B):
    """Element-wise sum of two matrices. Return None on dimension mismatch."""
    if not A or not B or len(A) != len(B) or len(A[0]) != len(B[0]):
        print("Cannot add: dimension mismatch.")
        return None

    rows = len(A)
    cols = len(A[0])
    return [[A[i][j] + B[i][j] for j in range(cols)] for i in range(rows)]


def matrix_transpose(matrix):
    """Transpose using nested list comprehension and zip(*matrix)."""
    # zip(*matrix) groups columns together; wrap in list comprehension
    return [[val for val in col] for col in zip(*matrix)]


def matrix_multiply(A, B):
    """
    Matrix multiplication A x B using dot-product logic.
    Return None on dimension mismatch.
    """
    if not A or not B or len(A[0]) != len(B):
        print("Cannot multiply: A's columns must equal B's rows.")
        return None

    # For each row in A and each column in B (via zip(*B))
    return [
        [
            sum(a * b for a, b in zip(row_a, col_b))
            for col_b in zip(*B)
        ]
        for row_a in A
    ]


if __name__ == "__main__":
    # Example 1: 2x2 matrices
    a = [[1, 2], [3, 4]]
    b = [[5, 6], [7, 8]]

    print("A + B:", matrix_add(a, b))
    print("Transpose of A:", matrix_transpose(a))
    print("A x B:", matrix_multiply(a, b))

    # Example 2: 2x3 and 3x2 matrices
    c = [[1, 2, 3], [4, 5, 6]]      # 2x3
    d = [[7, 8], [9, 10], [11, 12]]  # 3x2

    print("C x D:", matrix_multiply(c, d))