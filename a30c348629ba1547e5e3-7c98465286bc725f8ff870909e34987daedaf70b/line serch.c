#include <stdio.h>

# liner serch
int lookup(char *word, char *array[]) {
  int i;
  for (i = 0; array[i] != NULL; i++) {
    if (strcmp(word, array[i]) == 0)
      return i;
  }
  return -1;
}

int main (int argc, const char * argv[])
{
  char *flab[] = {
    "test",
    "hoge",
    "ukita",
    "ukitazume",
    NULL
  };

  char *target = "ukitazume";
  int result = lookup(target, flab);
  printf("%d", result);


  return 0;
}
