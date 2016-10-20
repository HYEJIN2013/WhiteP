#include <stdio.h>

int bubble(int array[], size_t size);

int main(void)
{

  int i;
  size_t size;
  int array[7] = { 3, 9, 4, 6, 2, 8, 5 };
  //int array[5] = { 5, 4, 3, 2, 1 };
  int runs;
  size = sizeof(array)/sizeof(array[0]);

  printf("size: %zu\n", size);
  runs = bubble(array, size);

  for(i = 0; i < size; i++) {
    printf("%d\n", array[i]);
  }

  printf("%d runs\n", runs);

  return 0;
}

int bubble(int array[], size_t size) {
  int i, tmp, correct = 0;
  int runs = 0;

  while(!correct) {
    correct = 1;
    for(i = 0; i < size-1; i++) {
    runs++;
      if(array[i] > array[i+1]) {
        correct = 0;
        tmp = array[i+1];
        array[i+1] = array[i];
        array[i] = tmp;
      }
    }
  }

  return runs;
}
