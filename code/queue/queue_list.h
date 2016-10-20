#ifndef QUEUE_LIST_H
#define QUEUE_LIST_H

typedef ... data_t;

typedef struct node {
  data_t data;
  struct node *next;
} node;

typedef struct {
  node *front, *rear;
} queue_t;

/* Create a new LL node */
node *CreateNode(data_t data);

queue_t *Initialize();
int Empty(queue_t *queue);
void Enqueue(queue_t *queue, data_t data);
node *Dequeue(queue_t *queue, data_t *save);

#endif
