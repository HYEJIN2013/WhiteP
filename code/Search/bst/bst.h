/**
   Binary Search Tree (BST) implementation
   -------------
   Note: Any node-changes(add, delete node, ...)
   // I all parse the pointer to pointer into function
 **/
#ifndef BST_H
#define BST_H

#include <stdbool.h>

typedef ... data_t;

typedef struct BinaryNode {
    data_t data;
    struct BinaryNode* left;
    struct BinaryNode* right;
} BinaryNode;

typedef struct BST {
    BinaryNode* root;
} BST;

/* Initialize a bst */
// return a pointer to an empty bst
BST* CreateBST();

/* Check if a BST is empty */
bool IsEmpty(BST* tree);

/* Check if a node is a leaf */
bool IsLeaf(BinaryNode* node);

/* Search */
// return want-to-find node
BinaryNode* Search(BinaryNode* root, data_t key);

/* Insert a new node */
void InsertNode(BinaryNode** root, data_t data);

/* Delete node */
void DeleteNode(BinaryNode** root, data_t key);

/* Delete the min-value node (leftmost node) */
// return the value of deleted node
data_t DeleteMin(BinaryNode** root);

/* Delete the whole bst */
// need to be called before terminating program
void DeleteBST(BinaryNode** root);


/* Traversal */
/* Depth-first search (DFS) */
void InorderPrint(BinaryNode* root);
void PostorderPrint(BinaryNode* root);
void PreorderPrint(BinaryNode* root);

#endif