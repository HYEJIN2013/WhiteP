#include <stdio.h>
#include <assert.h>
#include <stdlib.h>
#include "queue_list.h"

node *CreateNode(data_t data)
{
  node *NewNode = (node*)malloc(sizeof(node));
  assert(NewNode != NULL);
  
  NewNode->data = data;
  NewNode->next = NULL;

  return NewNode;
}

queue_t *Initialize()
{
  queue_t *queue = (queue_t*)malloc(sizeof(queue_t));
  assert(queue != NULL);
  
  queue->front = queue->rear = NULL;

  return queue;
}

int Empty(queue_t *queue)
{
  return queue->front == NULL;
}

void Enqueue(queue_t *queue, data_t data)
{
  // Create a new LL node
  node *NewNode = CreateNode(data);

  // Queue is empty --> new node is both front and rear
  if(Empty(queue)) {
    queue->front = queue->rear = NewNode;
    return;
  }

  // Add the new node at the end of queue
  // and change rear
  queue->rear->next = NewNode;
  queue->rear = NewNode;
}

node *Dequeue(queue_t *queue, data_t *save)
{
  // Queue is empty --> return NULL
  if(Empty(queue)) {
    printf("Queue is empty.\n");
    return NULL;
  }

  // save the data
  *save = queue->front->data;
  
  // Store previous front and move front one node ahead
  node *temp = queue->front;
  queue->front = queue->front->next;
  free(temp);

  // if front becomes NULL --> change rear as NULL, too
  if(queue->front == NULL) {
    queue->rear = NULL;
  }

  return queue->front;
}
