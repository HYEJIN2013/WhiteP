#include <stdio.h>
#include <stdlib.h>
#include "queue_circular.h"

void Initialize(queue_t *queue)
{
  queue->rear = 0;
  queue->front = 0;
}

int Empty(queue_t queue)
{
  return queue.front == queue.rear;
}

int Full(queue_t queue)
{
  return (queue.rear - queue.front + 1) %
    MAX_QUEUE_SIZE == 0;
}

void Enqueue(queue_t *queue, data_t data)
{
  if(!Full(*queue)) {
    queue->rear = (queue->rear + 1) % MAX_QUEUE_SIZE;
    // in cicle 0 -> MAX_QUEUE_SIZE - 1
    queue->data[queue->rear] = data;
  } else {
    printf("Queue is full.\n");
  }
}

data_t Dequeue(queue_t *queue)
{
  if(!Empty(*queue)) {
    queue->front = (queue->front + 1) % MAX_QUEUE_SIZE;
    // in circle 0 -> MAX_QUEUE_SIZE - 1
    return queue->data[queue->front];
  } else {
    printf("Queue is empty.\n");
    exit(0);
  }
}
