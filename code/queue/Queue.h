# include <stdio.h>
# include <stdlib.h>
# include <string.h>

// #define MAXSIZE 20

typedef struct node {
	char data[MAXSIZE];
	struct node *link;
}Node;

typedef struct queue {
	Node *front;
	Node *rear;
}Queue;

void insert(Queue *q, char* value)
{
	Node *temp;
	temp=(Node *)malloc(sizeof(Node));
	if(temp==NULL)
	{
		printf("No Memory available Error\n");
		exit(0);
	}
    strncpy(temp->data, value, MAXSIZE);
	temp->link=NULL;
	if(q->rear == NULL)
	{
		q->rear = temp;
		q->front = q->rear;
	}
	else
	{
		q->rear->link = temp;
		q->rear = temp;
	}
}

int isEmpty(Queue *q)
{
	if((q->front == q->rear) && (q->rear == NULL))
	{
        return 1;
    }
    return 0;
}

void delete(Queue *q, char* value)
{
	Node *temp;
	if(isEmpty(q))
	{
		printf("The queue is empty, no item to delete.\n");
        return;
	}
    strncpy(value, q->front->data, MAXSIZE);
    printf("%s delete from queue.\n",value);
	temp = q->front;
	q->front = q->front->link;
	if(q->rear == temp){
	    q->rear = q->rear->link;
    }
	free(temp);
}

void list(Queue *q)
{
    Node *temp;
    temp = q->front;
	if(isEmpty(q))
	{
		printf("The queue is empty.\n");
        return;
	}
    while(temp!= NULL){
        printf("%s ", temp->data);
        temp = temp->link;
    }
}

