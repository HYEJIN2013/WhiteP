/*Populating Next Right Pointers in Each Node*/
/*
Problem:
Given a binary tree
struct TreeLinkNode {
    TreeLinkNode *left;
    TreeLinkNode *right;
    TreeLinkNode *next;
}
Populate each next pointer to point to its next right node. If there is no next right node, 
the next pointer should be set to NULL.
Initially, all next pointers are set to NULL.
*/

//This is a DFS based approach (look at the online solution first and then wrote it down):
//My initial thought on this problem is the maintain a "level" (as a argument) while DFS or 
//BFS traversing the tree. I finially did not implement my idea since the function prototype 
//given by the origianl problem statement does not contain an argument.  

void PopulatingPointers::connect(TreeNode *root)
{
  if(!root)
		return;
	if(root->left)
		root->left->next = root->right;
	if(root->right)
		root->right->next = root->next ? root->next->left:NULL;
	connect(root->left);
	connect(root->right);
}

//Another iterative solution (Non-recursive):
//In general, below is a nice post that discusses how to change a recursive function to an iterative one:
//http://stackoverflow.com/questions/12468251/convert-recursion-to-iteration
void PopulatingPointers::connectIterative(TreeNode *root)
{
	TreeNode *currPar = root;
	currPar->next = NULL;
	while(currPar){
		TreeNode *currLeft = currPar->left;            
		TreeNode *currCross = currPar;             //    *----->*   //currCross is initialy at the first *
		                                           //   / \    / \  //
		while(currCross){                          //  *-->*->*-->* //currLeft is initialy at the first *
			if(currLeft != currCross->left)
			   currLeft->next = currCross->left;
			
			currLeft = currLeft->next;
			if(currLeft)
			   currLeft->next = currCross->right;
	
			currCross = currCross->next;
		}
        currPar = currPar->left;
	}
}

//Summary:
//The above question is a tree iterate/traverse problem, it is important for
//undertanding the tree struture. Combine with the tree traverse algorithms
//in the Step1Practice and understand this well.  In general, when doing this sort
//of problems you need keep the pointer to a parent and a child node. Sometimes
//you may even need to keep the grand children node. (e.g., tree rotation.)
//Also,  keep in mind the following:
//1. is there auxiliary stack or queue can be used? If not, in what order should the
//tree be traversed? In the above example, you can not go back once you go down since
//there is no parent pointers. So you need to maintain the parent pointer and also the 
//leftmost node to start a new level (by retriving the left child of the prvious left).
//2. What the feature of the node that has just been traversed? E.g., does it has a 
//left/right child?  This tells you about important information such as where you have
//reached the tree.
