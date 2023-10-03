import sys
import time
import numpy
import multiprocessing
# from array_sum import array_sum_parallel

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
    print(offset)
    prefix_sum_recursive(arr_src, arr_dst, start, end, offset)
    return arr_dst


def prefix_sum_parallel(arr):
    num_processes = multiprocessing.cpu_count()
    chunk_size = len(arr) // num_processes if len(arr) > num_processes else 2

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
