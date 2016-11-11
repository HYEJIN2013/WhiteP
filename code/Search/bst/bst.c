#include <stdlib.h>
#include "bst.h"

BST* CreateBST()
{
  BST* tree = malloc(sizeof(BST));
  tree->root = NULL;

  return tree;
}

bool IsEmpty(BST* tree)
{
  return tree->root == NULL;
}

bool IsLeaf(BinaryNode* node)
{
  if(node != NULL) {
    return node->left == NULL && node->right == NULL;
  } else {
    return false;
  }
}

BinaryNode* Search(BinaryNode* root, data_t key)
{
  if(root == NULL) return NULL; // not found
  else if(root->data == key) return root; // found
  else if(root->data > key)
    // continue searching on the left sub-tree
    return Search(root->left, key);
  else // root->data < key
    // continue searching on the right sub-tre
    return Search(root->right, key);
}

void InsertNode(BinaryNode** root, data_t data)
{
  if(*root == NULL) {
    // create a new node
    BinaryNode* NewNode = malloc(sizeof(BinaryNode));
    NewNode->data = data;
    NewNode->left = NULL;
    NewNode->right = NULL;

    // assign root to new node
    *root = NewNode;
  } else if((**root).data > data) {
    // continue with left sub-tree
    InsertNode(&(*root)->left, data);
  } else { // root->data < data 
    // coninue with right sub-tree
    InsertNode(&(*root)->right, data);
  }
}

void DeleteNode(BinaryNode** root, data_t key)
{
  if(*root != NULL) {
    if((**root).data > key)
      DeleteNode(&(*root)->left, key);
    else if((**root).data < key)
      DeleteNode(&(*root)->right, key);
    else { // root->data == key
      // Delete a leaf
      if(IsLeaf(*root)) {
	free(*root);
	*root = NULL;
      }

      // Delete an inter-node has 1 right sub-tree
      else if((**root).left == NULL) {
	BinaryNode* temp = *root;
	*root = (**root).right;
	free(temp);
      }
      
      // Delete an inter-node has 1 left sub-tree
      else if((**root).right == NULL) {
	BinaryNode* temp = *root;
	*root = (**root).left;
	free(temp);
      }

      // Delete an inter-node has 2 sub-tree
      else {
	// I want to delete a from bst like this:
	//       a
	//      / \
	//     b   c
	//        / \
	//       d   e
	// with data of: b < a < d < c < e
	// if we want to delete a
	// then: b < d < c < e
	// (d: leftmost node of right-sub tree)
	// --> swap data of a with d -> delete d
	(**root).data = DeleteMin(&(*root)->right);
      }
    }
  }
}

data_t DeleteMin(BinaryNode** root)
{
  data_t save;

  if((**root).left == NULL) {
    save = (**root).data;
    DeleteNode(root, save); // selft destruct
    return save;
  } else {
    return DeleteMin(&(*root)->left);
  }
}

void DeleteBST(BinaryNode** root)
{
  if(*root != NULL) {
    DeleteBST(&(*root)->left);
    DeleteBST(&(*root)->right);
    free(*root);
  }
}


/* Traversal */
void InorderPrint(BinaryNode* root)
{
  if(root != NULL) {
    InorderPrint(root->left);
    printf("...", root->data);
    InorderPrint(root->right);
  }
}

void PostorderPrint(BinaryNode* root)
{
  if(root != NULL) {
    PostorderPrint(root->left);
    PostorderPrint(root->right);
    printf("...", root->data);
  }
}

void PreorderPrint(BinaryNode* root)
{
  if(root != NULL) {
    printf("...", root->data);
    PreorderPrint(root->left);
    PreorderPrint(root->right);
  } 
}