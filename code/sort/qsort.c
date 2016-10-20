#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

int* intcat( int* a1, int size1, int* a2, int size2 ) {
  int *result = malloc((size1+size2)*sizeof(int));
  int *iter = result;
  for ( int i = 0; i < size1; i++ ) { *iter++ = *a1++; }
  for ( int i = 0; i < size2; i++ ) { *iter++ = *a2++; }
  return result;
}

void print_array( int* array, int size ) {
  printf("[");
  for ( int i = 0; i < size; i++ ) {
    printf("\"%d\"", array[i]);
    if ( i < size-1 ) { printf(", "); }
  }
  printf("]\n");
}

int* quicksort( int *array, int size ) {

  if ( size <= 1 ) { return array; }

  if ( size == 2 ) {
    if ( array[0] < array[1] ) {
      return array;
    } else {
      int tmp = array[0];
      array[0] = array[1];
      array[1] = tmp;
      return array;
    }
  }

  int index = array[0];
  int left_size = 0;
  for ( int i = 1; i < size; i++ ) {
    if ( index >= array[i] ) { left_size++; }
  }
  left_size++;
  int right_size = size - left_size;

  int* left = malloc(left_size*sizeof(int));
  int* right = malloc(right_size*sizeof(int));

  int* left_iter = left;
  int* right_iter = right;

  for ( int i = 1; i < size; i++ ) {
    if ( index >= array[i] ) {
      *left_iter++ = array[i];
    } else {
      *right_iter++ = array[i];
    }
  }
  *left_iter = index;
  return intcat(  quicksort(left, left_size),
                  left_size,
                  quicksort(right, right_size),
                  right_size );
}


int main( int argc, char** argv ) {
  int array[15] = { 14,13,12,11,10,5,7,3,6,2,9,0,4,8,1 };
  int* sorted = quicksort( array, 15 );
  print_array( sorted, 15 );
}
