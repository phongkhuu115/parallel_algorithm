import time
import numpy as np
import multiprocessing

def split_mat(A):
    n = A.shape[0]
    m = n // 2

    top_left = A[:m, :m]
    top_right = A[:m, m:]
    bottom_left = A[m:, :m]
    bottom_right = A[m:, m:]

    return [top_left, top_right, bottom_left, bottom_right]

def split_into_16(A):
    split_A= [[] for x in range(4)]
    for index, matrix in enumerate(split_mat(A)):
        if index == 0 or index == 1:
            split_A[0].append(split_mat(matrix)[0])
            split_A[0].append(split_mat(matrix)[1])
            split_A[1].append(split_mat(matrix)[2])
            split_A[1].append(split_mat(matrix)[3])
        else:
            split_A[2].append(split_mat(matrix)[0])
            split_A[2].append(split_mat(matrix)[1])
            split_A[3].append(split_mat(matrix)[2])
            split_A[3].append(split_mat(matrix)[3])

    return split_A


def strassen_multiply(args):
    A, B = args
    n = len(A)
    A = pad_to_power_of_two(A)
    B = pad_to_power_of_two(B)

    if len(A) <= 128:
        # return block_multiply(A,B)
        return A @ B

    # Phân rã ma trận thành các khối con
    A11, A12, A21, A22 = split_mat(A)
    B11, B12, B21, B22 = split_mat(B)

    # Tính các ma trận phụ
    M1 = strassen_multiply((A11 + A22, B11 + B22))
    M2 = strassen_multiply((A21 + A22, B11))
    M3 = strassen_multiply((A11, B12 - B22))
    M4 = strassen_multiply((A22, B21 - B11))
    M5 = strassen_multiply((A11 + A12, B22))
    M6 = strassen_multiply((A21 - A11, B11 + B12))
    M7 = strassen_multiply((A12 - A22, B21 + B22))

    # Tính các khối con của ma trận kết quả
    C11 = M1 + M4 - M5 + M7
    C12 = M3 + M5
    C21 = M2 + M4
    C22 = M1 - M2 + M3 + M6

    # Ghép các khối con thành ma trận kết quả
    C = np.vstack((np.hstack((C11, C12)), np.hstack((C21, C22))))
    return C[:n, :n]

def benchmark_strassen(args):
    return strassen_multiply(args)


def smallest_power_of_2(x):
    return 1 << (x - 1).bit_length()


def pad_to_power_of_two(matrix):
    n = matrix.shape[0]
    power_of_two = int(smallest_power_of_2(n))  # Find the next power of two

    pad_width = ((0, power_of_two - n), (0, power_of_two - n))  # Calculate pad width

    padded_matrix = np.pad(matrix, pad_width, mode="constant", constant_values=0)

    return padded_matrix

def parallel_multiply_matrices(matrix_a, matrix_b):
    A = split_into_16(matrix_a)
    B = split_into_16(matrix_b)
    pairs = [
        (A[0][0], B[0][0]),
        (A[0][1], B[1][0]),
        (A[0][2], B[2][0]),
        (A[0][3], B[3][0]),
        (A[0][0], B[0][1]),
        (A[0][1], B[1][1]),
        (A[0][2], B[2][1]),
        (A[0][3], B[3][1]),
        (A[0][0], B[0][2]),
        (A[0][1], B[1][2]),
        (A[0][2], B[2][2]),
        (A[0][3], B[3][2]),
        (A[0][0], B[0][3]),
        (A[0][1], B[1][3]),
        (A[0][2], B[2][3]),
        (A[0][3], B[3][3]),
        (A[1][0], B[0][0]),
        (A[1][1], B[1][0]),
        (A[1][2], B[2][0]),
        (A[1][3], B[3][0]),
        (A[1][0], B[0][1]),
        (A[1][1], B[1][1]),
        (A[1][2], B[2][1]),
        (A[1][3], B[3][1]),
        (A[1][0], B[0][2]),
        (A[1][1], B[1][2]),
        (A[1][2], B[2][2]),
        (A[1][3], B[3][2]),
        (A[1][0], B[0][3]),
        (A[1][1], B[1][3]),
        (A[1][2], B[2][3]),
        (A[1][3], B[3][3]),
        (A[2][0], B[0][0]),
        (A[2][1], B[1][0]),
        (A[2][2], B[2][0]),
        (A[2][3], B[3][0]),
        (A[2][0], B[0][1]),
        (A[2][1], B[1][1]),
        (A[2][2], B[2][1]),
        (A[2][3], B[3][1]),
        (A[2][0], B[0][2]),
        (A[2][1], B[1][2]),
        (A[2][2], B[2][2]),
        (A[2][3], B[3][2]),
        (A[2][0], B[0][3]),
        (A[2][1], B[1][3]),
        (A[2][2], B[2][3]),
        (A[2][3], B[3][3]),
        (A[3][0], B[0][0]),
        (A[3][1], B[1][0]),
        (A[3][2], B[2][0]),
        (A[3][3], B[3][0]),
        (A[3][0], B[0][1]),
        (A[3][1], B[1][1]),
        (A[3][2], B[2][1]),
        (A[3][3], B[3][1]),
        (A[3][0], B[0][2]),
        (A[3][1], B[1][2]),
        (A[3][2], B[2][2]),
        (A[3][3], B[3][2]),
        (A[3][0], B[0][3]),
        (A[3][1], B[1][3]),
        (A[3][2], B[2][3]),
        (A[3][3], B[3][3]),
    ]

    pairs = multiprocessing.Pool(multiprocessing.cpu_count()).map(benchmark_strassen, pairs)
    pairs = [sum(pairs[i:i+4]) for i in range(0, len(pairs), 4)]
    combined_array = np.vstack((
        np.hstack((pairs[0], pairs[1], pairs[2], pairs[3])),
        np.hstack((pairs[4], pairs[5], pairs[6], pairs[7])),
        np.hstack((pairs[8], pairs[9], pairs[10], pairs[11])),
        np.hstack((pairs[12], pairs[13], pairs[14], pairs[15]))
    ))

    return combined_array


if __name__ == "__main__":
    n = 1000
    A = np.random.randint(0, 10, size=(n, n))
    B = np.random.randint(0, 10, size=(n, n))
    # start = time.perf_counter()
    C = A @ B
    # end = time.perf_counter()
    start = time.perf_counter()
    C_dst = parallel_multiply_matrices(A, B)
    end = time.perf_counter()
    print(end - start)
    print(C_dst == C)