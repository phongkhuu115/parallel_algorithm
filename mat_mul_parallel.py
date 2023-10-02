import multiprocessing
import random
import sys
import time
import numpy as np


# test result of matrix multiplication
def test(A, B, C):
    return np.array_equal(np.dot(A, B), C)

def split_matrix(matrix):
    n = matrix.shape[0]
    half = n // 2
    A = matrix[:half, :half]
    B = matrix[:half, half:]
    C = matrix[half:, :half]
    D = matrix[half:, half:]
    return A, B, C, D

def strassen_multiply(A, B):
    start = time.perf_counter()
    if A.shape[0] <= 32:  # Sử dụng thuật toán nhân ma trận thông thường cho ma trận nhỏ
        return np.dot(A, B)

    # Phân rã ma trận thành các khối con
    A11, A12, A21, A22 = split_matrix(A)
    B11, B12, B21, B22 = split_matrix(B)

    # Tính các ma trận phụ
    M1 = strassen_multiply(A11 + A22, B11 + B22)
    M2 = strassen_multiply(A21 + A22, B11)
    M3 = strassen_multiply(A11, B12 - B22)
    M4 = strassen_multiply(A22, B21 - B11)
    M5 = strassen_multiply(A11 + A12, B22)
    M6 = strassen_multiply(A21 - A11, B11 + B12)
    M7 = strassen_multiply(A12 - A22, B21 + B22)

    # Tính các khối con của ma trận kết quả
    C11 = M1 + M4 - M5 + M7
    C12 = M3 + M5
    C21 = M2 + M4
    C22 = M1 - M2 + M3 + M6

    # Ghép các khối con thành ma trận kết quả
    C = np.vstack((np.hstack((C11, C12)), np.hstack((C21, C22))))
    end = time.perf_counter()
    # print("Strassen:", end-start, "s")
    return C


def parallel_strassen_multiply(args):
    A, B = args
    return strassen_multiply(A, B)


def fillRandom(A, B):
    for i in range(n):
        for j in range(n):
            A[i, j] = random.randrange(0, 10)
            B[i, j] = random.randrange(0, 10)


def saveToFile(A, B, C):
    np.set_printoptions(threshold=sys.maxsize)

    file = open("A.txt", "w")
   #  file.write("A:\n")
    file.write(str(A).replace('[', '{').replace(']', '}').replace(
        '.', ',').replace(',}', '},').replace('},}', '}}'))
    file.close()

    file = open("B.txt", "w")
   #  file.write("\nB:\n")
    file.write(str(B).replace('[', '{').replace(']', '}').replace(
        '.', ',').replace(',}', '},').replace('},}', '}}'))
    file.close()

    file = open("C.txt", "w")
   #  file.write("\nC:\n")
    file.write(str(C).replace('[', '{').replace(']', '}').replace(
        '.', ',').replace(',}', '},').replace('},}', '}}'))
    file.close()
    np.set_printoptions(threshold=10)




if __name__ == "__main__":
    threadNumber = 12
    pool = multiprocessing.Pool(threadNumber)
    
    n = 1024
    A = np.zeros((n, n))
    B = np.zeros((n, n))
    fillRandom(A, B)   
    
    part = int(len(A) / threadNumber)
    if part < 1:
        part = 1
    start = time.perf_counter()
    
    # C = strassen_multiply(A, B)
    C = pool.map(parallel_strassen_multiply, [(A, B)])
    # C = pool.map(parallel_strassen_multiply, [(i, A, B, part) for i in range(0, n, part)])
    
    end = time.perf_counter()
    # format output
    C = np.array(C).reshape(n, n)

    print("A:\n", A)
    print("B:\n", B)
    print("C:\n", C)
    print("SIZE:", n, "x", n)
    # print("test using numpy.dot:", test(A, B, C))

    print("Benmark", end-start, "s")
    # Chia công việc tính toán thành các khối con và sử dụng multiprocessing để song song hóa

    # saveToFile(A, B, C)
