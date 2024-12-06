def transpose(matrix):
    return list(map(list, zip(*matrix)))


def matrix_multiply(A, B):
    return [[sum(a * b for a, b in zip(A_row, B_col)) for B_col in transpose(B)] for A_row in A]


def inverse(matrix, tol=1e-10):
    size = len(matrix)
    identity = [[float(i == j) for i in range(size)] for j in range(size)]
    for i in range(size):
        # Check if the diagonal element is close to zero
        if abs(matrix[i][i]) < tol:
            matrix[i][i] += tol  # Regularization to avoid singularity
        factor = matrix[i][i]
        for j in range(size):
            matrix[i][j] /= factor
            identity[i][j] /= factor
        for k in range(size):
            if k != i:
                factor = matrix[k][i]
                for j in range(size):
                    matrix[k][j] -= factor * matrix[i][j]
                    identity[k][j] -= factor * identity[i][j]
    return identity


def multiregression(X, y):
    # Adding intercept column of ones to X
    X_b = [[1] + row for row in X]

    # Calculating transpose(X) * X
    X_b_T = transpose(X_b)
    X_b_T_X_b = matrix_multiply(X_b_T, X_b)

    # Calculating inverse of (X_b_T_X_b) with regularization
    X_b_T_X_b_inv = inverse(X_b_T_X_b)

    # Calculating transpose(X) * y
    X_b_T_y = matrix_multiply(X_b_T, [[value] for value in y])

    # Calculating theta (coefficients)
    theta = matrix_multiply(X_b_T_X_b_inv, X_b_T_y)
    return [value[0] for value in theta]


# Sample data
X = [[1, 2], [2, 3], [3, 5], [4, 7]]
y = [1, 2, 2.5, 3.5]

# Calculate coefficients
coefficients = multiregression(X, y)
print("Coefficients:", coefficients)