/*
 * flat.c
 *
 *  Created on: Apr 16, 2016
 *      Author: kkim
 */

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>
#include <stdarg.h>

typedef enum {
    STRING,
    LIST
} Type;

typedef struct any {
    void * value;
    Type type;
} Any;

typedef struct Node{
    Any *value;
    struct Node * next;
} Node;


typedef struct List {
    Node *head;
    Node *tail;
} List;

void memory_allocation_error() {
    fprintf(stderr,"memory allocation error");
    exit(-1);
}


void * check_null(void *value) {
    if(!value)
        memory_allocation_error();
    return value;
}

#define new_of(TYPE) (TYPE*) check_null(calloc(1,sizeof(TYPE)))


Any *new_any() {
    return new_of(Any);
}

Node *new_node() {
    return new_of(Node);
}

List *new_list() {
    return new_of(List);
}


Any *anydup(Any *any) {
    Any *new = new_any();
    new->value = any->value;
    new->type = any->type;

    return new;
}

Node *nodedup(Node *node) {
    Node *new = new_node();
    new->value=anydup(node->value);
    return new;
}

Any * any_value(void *value,Type type) {
    Any *new=new_any();
    new->value=value;
    new->type=type;
    return new;
}

void list_insert_node(List *self,Node *node) {
    if (self==NULL || node==NULL)
        return;

    if (self->tail==NULL) {
        assert(self->head==NULL);
        self->head = node;
        self->tail = node;
    } else {
        self->tail->next = node;
        self->tail=node;
    }
}

void list_insert_value(List *self,Any *value) {
    Node *node;
    if(self == NULL || value == NULL)
        return;

    node = new_node();
    node->value = anydup(value);
    list_insert_node(self,node);
}

List *new_list_with(List* val,...) {
    Any *v=NULL;
    va_list va;

    if(val==NULL)
        return val;

    va_start(va,val);
    while((v=va_arg(va, Any *))!=NULL) {
        list_insert_value(val,v);
    }
    va_end(va);

    return val;
}


void print_list(FILE *,List*);

void print_any(FILE *out, Any *any) {

    if(out==NULL || any==NULL)
        return;

    switch (any->type) {
    case STRING:
        fprintf(out,"%s",(char*)any->value);
        break;
    case LIST:
        print_list(out,(List*)any->value);
    }
}

void print_list(FILE *out,List *list) {
    Node *node=NULL;

    if(out==NULL || list==NULL)
        return;

    node=list->head;
    fprintf(out,"[");
    while(node!=NULL) {
        print_any(out,node->value);
        node = node->next;
        if(node!=NULL) {
            fprintf(out,",");
        }
    }
    fprintf(out,"]");
}

#define append list_insert_value

void node_memory_free(Node *node) {
    if (node==NULL)
        return;

    if(node->value) {
        free(node->value);
        node->value=NULL;
    }

    free(node);
}

void list_memory_free(List *list) {
    Node *node = NULL;
    Node *next = NULL;

    if(list==NULL)
        return;

    node = list->head;

    while(node!=NULL) {
        next = node->next;
        node_memory_free(node);
        node = next;
    }

    free(list);
}

#define node_type(NODE)  (NODE->value->type)
#define node_type_is(NODE,TYPE) (NODE->value && node_type(NODE) == TYPE)
#define node_value(NODE) (NODE->value->value)


void flat(List *list,List *output) {
    Node *node = NULL;

    if(list==NULL || output==NULL)
        return;

    node = list->head;

    while(node!=NULL) {
        if (node_type_is(node, LIST)) {
            flat((List*)node_value(node),output);
        } else if (node_type_is(node,STRING)) {
            append(output,anydup(node->value));
        }
        node = node->next;
    }
}

int main(int argc,char *argv[]) {


    List *lista,*listb,*listc,*listd,*data,*flat_list;

    lista = new_list_with(new_list(),any_value("a",STRING));
    listb = new_list_with(new_list(),any_value("b",STRING),any_value(lista,LIST));
    listc = new_list_with(new_list(),any_value("c",STRING),any_value(listb,LIST));
    listd = new_list_with(new_list(),any_value("d",STRING),any_value(listc,LIST));

    data = new_list();
    append(data,any_value(lista,LIST));
    append(data,any_value(listb,LIST));
    append(data,any_value(listc,LIST));
    append(data,any_value(listd,LIST));
    append(data,any_value("e",STRING));

    print_list(stdout,data);
    printf("\n");

    flat_list = new_list();
    flat(data,flat_list);
    print_list(stdout,flat_list);
    printf("\n");

    list_memory_free(data);
    list_memory_free(flat_list);
    list_memory_free(lista);
    list_memory_free(listb);
    list_memory_free(listc);
    list_memory_free(listd);

}
