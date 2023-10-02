

BASE_SIZE = 25
ONE_THOUSAND = 1000
ONE_TEN_HOUSAND = 10000
ONE_HUNDRED_THOUSAND = 100000
ONE_MILLION = 1000000
ONE_HUNDRED_MILLION = 100000000
ONE_BILLION = 1000000000


def benmark(size):
    # set print options
    np.set_printoptions(threshold=10)
    arr_src = np.random.randint(10, size=(size))
    start = time.time()
    arr_dst = prefix_sum_parallel(arr_src)
    end = time.time() - start
    print(np.array(arr_dst))
    print("Total: {}s".format(end))

   # benmark(BASE_SIZE)
    # benmark(ONE_THOUSAND)
    # benmark(ONE_MILLION)
    # benmark(ONE_HUNDRED_MILLION)
    # benmark(ONE_BILLION)
