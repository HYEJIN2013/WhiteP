""" SORTING"""

def less(x_value, y_value):
    """
    requires Transitive(x and y)
    """
    return x_value < y_value

def argmin(array, **kwargs):
    """ requires Transitive(x and y) """
    start = kwargs.get('start', 0)
    end = kwargs.get('end', len(array))
    cmp = kwargs.get('cmp', less)
    min_value = array[start]
    index = start
    while start < end:
        if cmp(array[start], min_value):
            min_value = array[start]
            index = start
        start += 1
    return index

def selection_sort(array, **kwargs):
    """ requres Transitive(x and y) """
    start = kwargs.get('start', 0)
    end = kwargs.get('end', len(array))
    cmp = kwargs.get('cmp', less)
    while start < end:
        i = argmin(array, start=start, end=end, cmp=cmp)
        array[i], array[start] = array[start], array[i]
        start += 1

def main():
    """ main """
    x_array = list(range(5000))
    selection_sort(x_array, start=0)

if __name__ == '__main__':
    main()
