import time
import numpy as np


def benmark_prefix_sum(size,  prefix_sum):
    # set print options
    np.set_printoptions(threshold=10)
    arr_src = np.random.randint(10, size=(size))
    start = time.perf_counter()
    arr_dst = prefix_sum(arr_src)
    end = time.perf_counter() - start
    print(np.array(arr_dst))
    print("Total: {}s".format(end))

def benmark_prefix_sum_debug(size,  prefix_sum):
    # set print options
    np.set_printoptions(threshold=10)
    arr_src = np.random.randint(10, size=(size))
    start = time.perf_counter()
    arr_dst = prefix_sum(arr_src)
    end = time.perf_counter() - start
    
    print(np.array(arr_src))
    print(np.array(arr_dst))
    
    print("Total: {}s".format(end))


def benmark_array_sum(size,  array_sum):
    # set print options
    np.set_printoptions(threshold=10)
    _input = np.random.randint(10, size=(size))
    start = time.perf_counter()
    _output = array_sum(_input)
    end = time.perf_counter() - start
    print(np.array(_output))
    print("Total: {}s".format(end))


def benmark_injection(function):
    start = time.perf_counter()
    _output = function()
    end = time.perf_counter() - start
    print(np.array(_output))
    print("Total: {}s".format(end))
    return _output
