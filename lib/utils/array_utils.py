#
# Simple array helper class
#
class ArrayUtils():
    #
    # Splits a given array based on the max values. For example: 
    # Arr: [20, 23, 55, 77, 86, 99, 106] 
    # Max: 5
    # Would result in the following arrays: 
    # 0: [20, 23, 55, 77, 86]
    # 1: [99, 106]
    #
    @staticmethod
    def _split_arr(arr, max):
        return [arr[i:i + max] for i in range(0, len(arr), max)]