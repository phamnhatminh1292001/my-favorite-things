import math
import numpy as np


def gram_schmidt(A):
    n, k = len(A), len(A[0])
    U = np.zeros((n, k))
    U[0, :] = A[0, :]
    for i in range(1, n):
        U[i, :] = A[i, :]
        for j in range(0, i):
            mu_ij = U[j, :].dot(U[i, :]) / U[j, :].dot(U[j, :])
            U[i, :] = U[i, :] - mu_ij * U[j, :]
    return U


basis = np.array(
    [
        np.array((4, 1, 3, -1)),
        np.array((2, 1, -3, 4)),
        np.array((1, 0, -2, 7)),
        np.array((6, 2, 9, -5)),
    ]
)

ortho = gram_schmidt(basis)
print(ortho)
print("{0:.5f}".format(ortho[3][1]))