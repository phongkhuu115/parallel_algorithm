import multiprocessing as mp
from multiprocessing import Process, Pool
import random
import sys
import time
import numpy as np
import os


def check(A, B, C):
    return np.array_equal(np.dot(A, B), C)


def split_matrix(matrix):
    n = matrix.shape[0]
    half = n // 2
    A = matrix[:half, :half]
    B = matrix[:half, half:]
    C = matrix[half:, :half]
    D = matrix[half:, half:]
    return A, B, C, D


def recursive_mat_mul(A, B):
    Z = []
    if len(A) <= 128:
        return A @ B

    X11, X12, X21, X22 = split_matrix(A)
    Y11, Y12, Y21, Y22 = split_matrix(B)

    Z11 = recursive_mat_mul(X11, Y11) + recursive_mat_mul(X12, Y21)
    Z12 = recursive_mat_mul(X11, Y12) + recursive_mat_mul(X12, Y22)
    Z21 = recursive_mat_mul(X21, Y11) + recursive_mat_mul(X22, Y21)
    Z22 = recursive_mat_mul(X21, Y12) + recursive_mat_mul(X22, Y22)

    Z = np.vstack((np.hstack((Z11, Z12)), np.hstack((Z21, Z22))))
    return Z

def benchmark_each(args):
    start = time.perf_counter()
    C = recursive_mat_mul(args)
    print(time.perf_counter() - start)
    return C


def parallel_multiply_matrices(matrix_a, matrix_b):

    X11, X12, X21, X22 = split_matrix(matrix_a)
    Y11, Y12, Y21, Y22 = split_matrix(matrix_b)

    pairs = [
        (X11, Y11),
        (X12, Y21),
        (X11, Y12),
        (X12, Y22),
        (X21, Y11),
        (X22, Y21),
        (X21, Y12),
        (X22, Y22),
    ]

    C = Pool(8).map(benchmark_each, pairs)

    Z = np.vstack((np.hstack((C[0] + C[1], C[2] + C[3])), np.hstack((C[4] + C[5], C[6] + C[7]))))
    return Z


if __name__ == "__main__":
    n = 5000
    A = np.random.randint(0, 10, size=(n, n))
    B = np.random.randint(0, 10, size=(n, n))
    res = []

    # start = time.perf_counter()
    # res = parallel_multiply_matrices(A, B)
    # end = time.perf_counter()

    start = time.perf_counter()
    res = recursive_mat_mul(A, B)
    end = time.perf_counter()

    print("A:\n", A)
    print("B:\n", B)
    print("Res:\n", res)
    print("SIZE:", n, "x", n)

    # print("Rightness:\n", res==A@B)

    print("Benchmark", end - start, "s")