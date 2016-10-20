#include "queue.h"

void init(int *head, int *tail) {
     *head = *tail = 0;
}

void push(int *q,int *tail, int element) {	
    q[(*tail)++] = element;
}

int pop(int *q,int *head) {	
     return q[(*head)++];
}

int empty(int head, int tail) {	
    if (head==tail) {
    	return 1;
    } else {
    	return 0;
    }
}