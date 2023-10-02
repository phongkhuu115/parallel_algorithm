import time
import numpy
import multiprocessing


def array_sum(arr_src):
    arr = arr_src
    n = len(arr)
    if n == 1:
        return arr[0]
    elif n == 2:
        return arr[0] + arr[1]
    else:
        mid = n // 2
        return array_sum(arr[:mid]) + array_sum(arr[mid:])


def array_sum_parallel(arr):
    num_processes = multiprocessing.cpu_count()
    chunk_size = len(arr) // num_processes

    with multiprocessing.Pool(processes=num_processes) as pool:
        chunks = [arr[i : i + chunk_size] for i in range(0, len(arr), chunk_size)]
        array_sums = pool.map(array_sum, chunks)


    return array_sum(array_sums)


BASE = 20
ONE_THOUSAND = 1000
ONE_MILLION = 1000000
TEN_MILLION = 1000000
ONE_HUNDRED_MILLION = 100000000
ONE_BILLION = 1000000000


def benmark(size):
    arr_src = numpy.random.randint(10, size=(size))
    start = time.time()
    sums = array_sum_parallel(arr_src)
    end = time.time() - start
    print(arr_src)
    print(sums)
    print("Parallel: {}s".format(end))

    # start = time.time()
    # print(array_sum(arr_src))
    # end = time.time() - start
    # print("Sequence: {}s".format(end))


# Example usage
if __name__ == "__main__":
    benmark(BASE)
    # benmark(ONE_THOUSAND)
    # benmark(ONE_MILLION)
    # benmark(TEN_MILLION)
    # benmark(ONE_HUNDRED_MILLION)
    # benmark(ONE_BILLION)
