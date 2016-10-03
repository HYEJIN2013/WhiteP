
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

void print_array(int *array, int start, int end)
{
    for (int i = start; i <= end; i++)
        printf("%d ", array[i]);
    printf("\n");
}

void swap(int *array, int i, int j)
{
    if (!array)
        return;

    int temp = array[i];
    array[i] = array[j];
    array[j] = temp;
}

int partition(int *array, int low, int high)
{
    int left = low;
    int right = high + 1;
    int pivot = array[low];

    while (true)
    {
        while (array[++left] < pivot)
            if (left == high)
                break;
        while (array[--right] > pivot)
            if (right == low)
                break;
        if (left < right)
            swap(array, left, right);
        else
            break;
    }
    swap(array, low, right);
    return right;
}

void sort(int *array, int low, int high)
{
    if (low >= high)
        return;
    int pivot = partition(array, low, high);
    sort(array, low, pivot - 1);
    sort(array, pivot + 1, high);
}

void quick_sort(int *array, int size)
{
    sort(array, 0, size - 1);
}

int main(void)
{
    int size;
    scanf("%d", &size);
    int array[size];
    for (int i = 0; i < size; i++)
        scanf("%d", &array[i]);
    quick_sort(array, size);
    print_array(array, 0, size - 1);
    return EXIT_SUCCESS;
}
