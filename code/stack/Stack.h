# include <stdio.h>
# include <stdlib.h>
# include <string.h>

// #define MAXSIZE 20

typedef struct node {
	char data[MAXSIZE];
	struct node *link;
}Node;

typedef struct stack {
	Node *top;
}Stack;

void insert(Stack *s, char* value)
{
	Node *temp;
	temp=(Node *)malloc(sizeof(Node));
	if(temp==NULL)
	{
		printf("No Memory available Error\n");
		exit(0);
	}
    strncpy(temp->data, value, MAXSIZE);
	temp->link = s->top;
	s->top = temp;
}

int isEmpty(Stack *s)
{
	if(!s->top)
	{
        return 1;
    }
    return 0;
}

void delete(Stack *s, char* value)
{
	Node *temp;
	if(isEmpty(s))
	{
		printf("The stack is empty, no item to delete.\n");
        return;
	}
    strncpy(value, s->top->data, MAXSIZE);
    printf("%s delete from stack.\n",value);
	temp = s->top;
	s->top = s->top->link;
	free(temp);
}

void list(Stack *s)
{
    Node *temp;
    temp = s->top;
	if(isEmpty(s))
	{
		printf("The stack is empty.\n");
        return;
	}
    while(temp!= NULL){
        printf("%s ", temp->data);
        temp = temp->link;
    }
}

