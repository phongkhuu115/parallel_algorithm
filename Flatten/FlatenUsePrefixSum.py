import numpy
import multiprocessing
import time

pr_count = multiprocessing.cpu_count()

# def assignArraySize(BASE_SIZE):
#     S = [0] * BASE_SIZE
#     for i in range(BASE_SIZE):
#         S[i] = len(A[i])


# def calculate_flaten(output, input, start, end, offsetArray):
#     for i in range(start, end):
#         output[i] = input[i] + offsetArray[i]


# def check_prefix(a, b):
#     if sum(a) == b[-1]:
#         return True
#     return False


def calculate_prefix_sum(input, start, end, output, offset):
    for i in range(start, end + 1):
        output[i] = input[i] + offset
        offset = output[i]


def divide_and_conquer_prefix_sum(input, output, start, end, threshold):
    if start == end:
        return
    if end - start <= threshold:
        calculate_prefix_sum(input, start, end, output, 0)


def check_flaten(input, output):
    input = numpy.ndarray.flatten(input)
    input = numpy.array(input)
    output = numpy.array(output)

    if numpy.equal(input, output).all():
        return True
    return False


def calculate_offsetarray(BASE_SIZE, S):
    OFFSET = [0] * BASE_SIZE

    divide_and_conquer_prefix_sum(
        S, OFFSET, 0, len(S) - 1, BASE_SIZE)
    OFFSET.pop()
    OFFSET.insert(0, 0)
    return OFFSET


def divide_and_conquer_flaten(args):
    input, offsetArray = args
    if len(input) == 1:
        return input[0]
    else:
        mid = len(input) // 2
        left = divide_and_conquer_flaten((input[:mid], offsetArray[:mid]))
        right = divide_and_conquer_flaten((input[mid:], offsetArray[mid:]))
        return concat_arrays(left, right)


def concat_arrays(*args):
    total_length = sum([len(x) for x in args])
    result = numpy.empty(total_length, dtype=args[0].dtype)
    start = 0
    for x in args:
        end = start + len(x)
        result[start:end] = x
        start = end
    return result


def calculate_optimal_chunksize(input_size, num_processors):
    return max(1, input_size // num_processors)


def flatten_parallel_executor(input, size):
    chunkSize = calculate_optimal_chunksize(size, pr_count)
    arraySizes = [len(input[i]) for i in range(size)]
    offsetArray = calculate_offsetarray(size, arraySizes)

    chunksInput = [input[i:i + chunkSize]
                   for i in range(0, len(input), chunkSize)]
    chunksOffset = [offsetArray[i:i + chunkSize]
                    for i in range(0, len(offsetArray), chunkSize)]

    parts = [(chunksInput[i], chunksOffset[i])
             for i in range(len(chunksInput))]

    pool = multiprocessing.Pool(processes=pr_count)
    res = pool.map(divide_and_conquer_flaten, parts)
    res = concat_arrays(*res)
    return res


if __name__ == '__main__':
    BASE_SIZE = 10000

    input = numpy.random.randint(0, 10, size=(
        BASE_SIZE, BASE_SIZE), dtype=numpy.int8)

    start = time.perf_counter()
    res = flatten_parallel_executor(input, BASE_SIZE)
    end = time.perf_counter() - start

    print('end: ', end)
    print('res: ', res)
    print(check_flaten(input, res))
