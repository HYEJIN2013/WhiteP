/* Enqueue and dequeue functions 
  have been written in such a way
  so as to ensure constant time operation,
  which is the case with a queue.
*/

#include <stdio.h>
#include <windows.h>

struct node{
	int data;
	struct node *link;
};

struct node *front = NULL;
struct node *rear = NULL;

void enqueue(int x)
{
	struct node *temp;
	temp = (struct node *)malloc(sizeof(struct node));
	temp->data = x;
	temp->link = NULL;
	if (front == NULL&&rear == NULL)
	{
		front = rear = temp;
		return;
	}
	rear->link = temp;
	rear = temp;
}

void dequeue()
{
	struct node *temp;
	temp = front;
	if (front == NULL)
	{
		return;
	}
	else if (front == rear)
	{
		front = rear = NULL;
	}
	else
		front = front->link;
	free(temp);
}

void print()
{
	struct node *temp;
	temp = front;
	while (temp != NULL)
	{
		printf("%d ", temp->data);
		temp = temp->link;
	}
	printf("\n");
}



int main(void)
{	
	enqueue(4);
	print();
	enqueue(6);
	print();
	enqueue(8);
	print();
	enqueue(9);
	print();
	dequeue();
	print();
	system("pause");
	return 0;
}
