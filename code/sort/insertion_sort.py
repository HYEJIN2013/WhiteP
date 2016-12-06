def insertion_sort(unsorted_list):
    """
    >>> unsorted_list = [5, 9, 2, 99, 3, 128, 3]
    >>> insertion_sort(unsorted_list)
    >>> unsorted_list
    [2, 3, 3, 5, 9, 99, 128]
    """

    for i in range(1, len(unsorted_list)):
        shift(unsorted_list, i)


def shift(unsorted_list, index):

    for i in range(0, index):

        if unsorted_list[index] < unsorted_list[i]:
            unsorted_list[index], unsorted_list[i] = unsorted_list[i], unsorted_list[index]


if __name__ == '__main__':
    import doctest
    doctest.testmod()
