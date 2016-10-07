#include <stdio.h>
#include <string.h>
typedef struct st {
    int data[10000];
    int size;
} Stack;

void initStack(Stack *st) {
    st->size = 0;
}
void push(Stack *st, int num) {
    st->data[(st->size)++] = num;
}
int empty(Stack *st) {
    return (st->size) == 0;
}
int pop(Stack *st) {
    if (empty(st)) {
        return -1;
    } else {
        return st->data[--(st->size)];
    }
}
int top(Stack *st) {
    if (empty(st)) {
        return -1;
    } else {
        return st->data[(st->size)-1];
    }
}

int main() {
    int n;
    scanf("%d", &n);

    Stack s;
    initStack(&s);

    while (n--) {
        char cmd[16];
        scanf("%s", cmd);
        if (strcmp(cmd, "push") == 0) {
            int num;
            scanf("%d", &num);
            push(&s, num);
        }
        else if (strcmp(cmd, "top") == 0) {
            printf("%d\n", empty(&s) ? -1 : top(&s));
        }
        else if (strcmp(cmd, "size") == 0) {
            printf("%d\n", s.size);
        }
        else if (strcmp(cmd, "empty") == 0) {
            printf("%d\n", empty(&s));
        }
        else if (strcmp(cmd, "pop") == 0) {
            printf("%d\n", empty(&s) ? -1 : top(&s));
            if (!empty(&s)) {
                pop(&s);
            }
        }
    }
    return 0;
}
