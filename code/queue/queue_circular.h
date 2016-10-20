#ifndef QUEUE_CIRCULAR_H
#define QUEUE_CIRCULAR_H

typedef ... data_t;
#define MAX_QUEUE_SIZE ...

typedef struct {
    data_t data[MAX_QUEUE_SIZE];
    int rear, front;
} queue_t;

void Initialize(queue_t *queue);
int Empty(queue_t queue);
int Full(queue_t queue);
void Enqueue(queue_t *queue, data_t data);
data_t Dequeue(queue_t *queue);

#endif
