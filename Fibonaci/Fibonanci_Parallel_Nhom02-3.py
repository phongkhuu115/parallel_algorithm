import multiprocessing as mp
import time

_FirstTenFib = {
    0: 1,
    1: 1,
    2: 2,
    3: 3,
    4: 5,
    5: 8,
    6: 13,
    7: 21,
    8: 34,
    9: 55,
    10: 89,
}


def Fibonanci(n):
    if n in _FirstTenFib:
        return _FirstTenFib.get(n)

    k = n >> 1

    fib_k = Fibonanci(k)
    fib_k_minus_1 = Fibonanci(k - 1)
    fib_k_plus_1 = Fibonanci(k + 1)
    _FirstTenFib.update({n:  (fib_k * fib_k_plus_1 + fib_k_minus_1 * fib_k) if n &  # type: ignore
                        1 else (fib_k * fib_k + fib_k_minus_1 * fib_k_minus_1)})  # type: ignore
    return _FirstTenFib[n]


def Det(a, b, c, d):
    return a * b + c * d


def Divine(n):

    if n & 1:
        P1 = n >> 1
        P2 = (n >> 1) + 1
        P3 = (n >> 1)
        P4 = (n >> 1) - 1

    else:
        P1 = n >> 1
        P2 = (n >> 1)
        P3 = (n >> 1) - 1
        P4 = (n >> 1) - 1
    return P1, P2, P3, P4


def parallel(n):
    if n in _FirstTenFib:
        return _FirstTenFib[n]
    n -= 1

    P = Divine(n)
    args = []

    for i in range(4):
        Si = Divine(P[i])
        args.extend(Si)

    raw = mp.Pool(8).map(Fibonanci, args)

    res = Det(
        Det(raw[0], raw[1], raw[2], raw[3]),
        Det(raw[4], raw[5], raw[6], raw[7]),
        Det(raw[8], raw[9], raw[10], raw[11]),
        Det(raw[12], raw[13], raw[14], raw[15])
    )
    return res


if __name__ == '__main__':
    n = "1000"

    n = int(n.replace(" ", ""))

    start_time = time.time()
    res = parallel(n)
    end_time = time.time()

    execution_time = end_time - start_time
    print(f"The {n}-th Fibonacci number is: {res}")
    print(f"The execution time: {execution_time} s")
