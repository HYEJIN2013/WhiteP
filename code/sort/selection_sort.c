/**
 *  http://pt.wikipedia.org/wiki/Selection_sort
 */

#include <stdio.h>
#define VL 5 // Tamanho do vetor

int main () {
  
  int v[6], indice, min, i, j;

  // Ler o vetor
  for (i = 0; i < VL; i++) {
    scanf("%d", &v[i]);
  }

  // Selection Sort
  for (j = 0; j < VL; j++) {

    // Ajustar variaveis para cada passo da varredura
    min = v[j];
    indice = j;

    // Pegar o menor elemento
    for (i = j; i < VL; i++) {
      if (v[i] < min) {
        min = v[i];
        indice = i;
      }
    }

    // Trocar elementos de posicao
    v[indice] = v[j];
    v[j] = min;

  }
  
  // Mostrar o vetor
  for (i = 0; i < VL; i++) {
    printf("%d\n", v[i]);
  }

  return 0;
}
