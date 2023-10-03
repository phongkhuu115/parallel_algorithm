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
        chunks = [arr[i: i + chunk_size]
                  for i in range(0, len(arr), chunk_size)]
        array_sums = pool.map(array_sum, chunks)
    return array_sum(array_sums)
