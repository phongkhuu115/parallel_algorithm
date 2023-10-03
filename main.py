import _TestCase as testcase
import importlib
from _Benmarker import benmark_array_sum
from _Benmarker import benmark_prefix_sum
from _Benmarker import benmark_prefix_sum_debug


from Sum.array_sum import array_sum_parallel
from Sum.prefix_sum import prefix_sum_parallel
importlib.import_module('Sum')
importlib.import_module('_Benmarker')



# Example usage
if __name__ == '__main__':

    SIZE_DEBUG = 10

    SIZE_EASY = testcase.ONE_THOUSAND
    SIZE_MEDIUM = testcase.ONE_HUNDRED_THOUSAND
    SIZE_HARD = testcase.ONE_MILLION
    SIZE_ULTRA_HARD = testcase.ONE_HUNDRED_MILLION
    SIZE_DOOM = testcase.ONE_BILLION

    # benmark_prefix_sum(SIZE_DEBUG, prefix_sum_parallel)
    benmark_prefix_sum_debug(SIZE_DEBUG, prefix_sum_parallel)
    # benmark_array_sum(SIZE_EASY, array_sum_parallel)
