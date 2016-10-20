#include <stdio.h>
#include <stdarg.h>

void bubble(char *item, int count);

main(void) {
    char str[11] = "ebdacfhgze";
    bubble(str, 10);
    printf("%s\n", str);
}

/* Bubble Sort */
void bubble(char *item, int count) {
    register int a, b;
    register char t;
    
    for (a = 0; a < count; ++a) {
        printf("a = %c, ", item[a]);
        for (b = count-1; b >= a; --b) {
            printf("b = %c\n", item[b]);
            if (item[b-1] > item[b]) {
                printf("b-1 = %c\n", item[b-1]);
                /* troca os elementos */
                t = item[b-1];
                item[b-1] = item[b];
                item[b] = t;
            }
        }
    }
}
