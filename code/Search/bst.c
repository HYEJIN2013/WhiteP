
#include<stdlib.h>
#include<stdio.h>

struct bin_tree {
int data;
struct bin_tree * right, * left;
};
typedef struct bin_tree node;

void insert(node ** tree, int val)
{
    node *temp = NULL;
    if(!(*tree))
    {
        temp = (node *)malloc(sizeof(node));
        temp->left = temp->right = NULL;
        temp->data = val;
        *tree = temp;
        return;
    }

    if(val < (*tree)->data)
    {
        insert(&(*tree)->left, val);
    }
    else if(val > (*tree)->data)
    {
        insert(&(*tree)->right, val);
    }

}

void print_preorder(node * tree)
{
    if (tree)
    {
        printf("%d\n",tree->data);
        print_preorder(tree->left);
        print_preorder(tree->right);
    }

}

void print_inorder(node * tree)
{
    if (tree)
    {
        print_inorder(tree->left);
        printf("%d\n",tree->data);
        print_inorder(tree->right);
    }
}

void print_postorder(node * tree)
{
    if (tree)
    {
        print_postorder(tree->left);
        print_postorder(tree->right);
        printf("%d\n",tree->data);
    }
}

void deltree(node * tree)
{
    if (tree)
    {
        deltree(tree->left);
        deltree(tree->right);
        free(tree);
    }
}

node* search(node ** tree, int val)
{
    if(!(*tree))
    {
        return NULL;
    }

    if(val < (*tree)->data)
    {
        search(&((*tree)->left), val);
    }
    else if(val > (*tree)->data)
    {
        search(&((*tree)->right), val);
    }
    else if(val == (*tree)->data)
    {
        return *tree;
    }
}

node* par(node ** tree, int val,node ** a)
{
   
    if(val < (*tree)->data)
    {
    *a=*tree;
        par(&((*tree)->left), val,a);
    }
    else if(val > (*tree)->data)
    {
    *a=*tree;
        par(&((*tree)->right), val,a);
    }
    else if(val == (*tree)->data)
    {
        return *a;
    }
}
/* deletes a node from the binary search tree */
node* delnode ( node ** tree, int num )
{
   
    node *parent, *x, *xsucc ;

    /* if tree is empty */
if ( *tree == NULL )
    {
        printf ( "\nTree is empty" ) ;
        return ;
    }

    parent = x = NULL ;

    /* call to search function to find the node to be deleted */

    x=search (tree, num) ;

    /* if the node to deleted is not found */
if (!x)
    {
        printf ( "\nData to be deleted, not found\n" ) ;
        return ;
    }

    /* if the node to be deleted has two children */
if ( x -> left != NULL && x -> right != NULL )
    {
        parent = x ;
        xsucc = x -> right ;

        while ( xsucc -> left != NULL )
        {
            parent = xsucc ;
            xsucc = xsucc -> left ;
        }

        x -> data = xsucc -> data ;
        x = xsucc ;
    }

    /* if the node to be deleted has no child */
if ( x -> left == NULL && x -> right == NULL )
    {
         parent=par(tree,num,tree);
    if ( parent -> right == x )
            parent -> right = NULL ;
        else
            parent -> left = NULL ;

        free ( x ) ;
        return ;
    }

    /* if the node to be deleted has only rightchild */
if ( x -> left == NULL && x -> right != NULL )
    {
       
    parent=par(tree,num,tree);
   
    printf("HI\n");
        if ( parent -> left == x )
            {parent -> left = x -> right ;
             }
        else
            parent -> right = x -> right ;
   
        free ( x ) ;
        return ;
    }

    /* if the node to be deleted has only left child */
if ( x -> left != NULL && x -> right == NULL )
    {
    parent=par(tree,num,tree);
        if ( parent -> left == x )
            parent -> left = x -> left ;
        else
            parent -> right = x -> left ;

        free ( x ) ;
        return ;
    }
}
void main()
{
    node *root;
    node *tmp;
    int ch,data,ans;

    root = NULL;
 
 do
{
    printf("Enter choice\n");   
    scanf("%d",&ch);
    switch(ch)
    {
    case 1:
            printf("Enter data\n");
            scanf("%d",&data);
            insert(&root,data);
            break;
    case 2:
             /* Printing nodes of tree */
                printf("Pre Order Display\n");
              print_preorder(root);
           
                printf("In Order Display\n");
                print_inorder(root);

                printf("Post Order Display\n");
                print_postorder(root);
            break;

  
    case 3:
   
            /* Search node into tree */
            printf("Enter data\n");
            scanf("%d",&data);
            tmp = search(&root,data);
                if (tmp)
                       {
                    printf("Searched node=%d\n", tmp->data);
                          }
                else
                         {
                       printf("Data Not found in tree.\n");
                    }
            break;

    case 4:
           
            /* Deleting all nodes of tree */
                deltree(root);
            break;

    case 5:
            printf("Enter data\n");
            scanf("%d",&data);
            delnode(&root,data);
            break;
    }
 printf("Want more\n");
 scanf("%d",&ans);
 }while(ans==1);
}  