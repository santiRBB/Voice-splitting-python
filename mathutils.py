# /**
#  * <code>MathUtils</code> is a static class of some utility functions that may need
#  * to be used from multiple places.
#  * <p>
#  * There is no reason for this class to ever be instantiated.
#  *
#  * @author Santiago Martín Cortés
#  * @version 1.0
#  * @since 1.0
#  */


import math


class MathUtils:

    def __init__(self):
        pass

        # /**

    #  * Evaluate a Gaussian window function with the given mean range and standard deviation. The formula is:
    #  * <p>
    #  * <code>G(m1, m2, s) = e ^ [(-1 / 2) * ([m2 - m1] / s) ^ 2]</code>
    #  *
    #  * @param mean1 The low end of the mean range.
    #  * @param mean2 The high end of the mean range.
    #  * @param std The standard deviation.
    #  * @return The value of the Gaussian window function.
    #  */

    @staticmethod
    def gaussianWindow(mean1, mean2, std):
        fraction = (mean2 - mean1) / std
        exponent = - (fraction * fraction) / 2.0
        return math.exp(exponent)

    # /**
    #  * Get the index of the first occurrence of the maximum value in the given array.
    #  *
    #  * @param array The array whose max we will find.
    #  * @return The index of the first occurrence of the maximum value of the given array. Or,
    #  * -1 if the maximum value is float NEGATIVE_INFINITY} or the array has length 0.
    #  */

    @staticmethod
    def getMaxIndex(array):
        maxVal = -float('inf')
        maxIndex = -1

        i = 0
        while i < len(array):
            if array[i] > maxVal:
                maxVal = array[i]
                maxIndex = i
            i += 1

        return maxIndex
