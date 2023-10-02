import multiprocessing
import sys
import numpy
import time
import random


def lineMult(args):
    start, A, B, part = args
    n = len(A)
    C = numpy.zeros((n, n))
    for i in range(start, start + part):
        for k in range(n):
            for j in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C


def ikjMatrixProduct(A, threadNumber):
    n = len(A)
    pool = multiprocessing.Pool(threadNumber)
    part = int(len(A) / threadNumber)
    if part < 1:
        part = 1
    result = pool.map(lineMult, [(i, A, B, part) for i in range(0, n, part)])
    C = numpy.zeros((n, n))
    for matrix in result:
        C += matrix
    return C


def filledWithRandomNumbers(A, B):
    for i in range(n):
        for j in range(n):
            A[i, j] = random.randrange(0, 10)
            B[i, j] = random.randrange(0, 10)


def saveToFile(A, B, C):
    numpy.set_printoptions(threshold=sys.maxsize)

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
    numpy.set_printoptions(threshold=10)


if __name__ == "__main__":
    threadNumber = 10
    n = 10
    A = numpy.zeros((n, n))
    B = numpy.zeros((n, n))
    filledWithRandomNumbers(A, B)

    start = time.perf_counter()
    C = ikjMatrixProduct(A, threadNumber)
    end = time.perf_counter()

    print("A:\n", A)
    print("B:\n", B)
    print("C:\n", C)
    saveToFile(A, B, C)
    print("Benmark", end-start, "s")
