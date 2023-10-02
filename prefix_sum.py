import time
import numpy
import multiprocessing


def prefix_sum_recursive(arr_src, arr_dst, start, end, offset):
    if start == end:
        arr_dst[start] = arr_src[start] + offset
    else:
        mid = (start + end) // 2
        prefix_sum_recursive(arr_src, arr_dst, start, mid, offset)
        left_sum = arr_dst[mid]
        prefix_sum_recursive(arr_src, arr_dst, mid + 1, end, left_sum)


def calculate_prefix_sum(args):
    arr_src, arr_dst, start, end, offset = args
    prefix_sum_recursive(arr_src, arr_dst, start, end, offset)
    return arr_dst


def prefix_sum_parallel(arr):
    num_processes = multiprocessing.cpu_count()
    chunk_size = len(arr) // num_processes

    with multiprocessing.Pool(processes=num_processes) as pool:
        chunks = [arr[i:i + chunk_size]
                  for i in range(0, len(arr), chunk_size)]
        args = [(chunk, chunk, 0, len(chunk) - 1, 0) for chunk in chunks]
        prefix_sums = pool.map(calculate_prefix_sum, args)

    result = []
    prefix_sum_value = 0
    for prefix in prefix_sums:
        result.extend([val + prefix_sum_value for val in prefix])
        prefix_sum_value = result[-1]

    return result


BASE_SIZE = 10
ONE_THOUSAND = 1000
ONE_MILLION = 1000000
ONE_HUNDRED_MILLION = 100000000
ONE_BILLION = 1000000000


def benmark(size):
    arr_src = numpy.random.randint(10, size=(size))
    start = time.time()
    arr_dst = prefix_sum_parallel(arr_src)
    end = time.time() - start
    print(arr_src[0:9])

    print(arr_dst[0:9])
    print("Total: {}s".format(end))


# Example usage
if __name__ == '__main__':
    benmark(BASE_SIZE)
    # benmark(10000)
    # benmark(ONE_MILLION)
    # benmark(ONE_HUNDRED_MILLION)