#include <iostream>
using namespace std;

struct node{
	int data;
	struct node* left;
	struct node* right;
};

struct node* newNode(int data){
	struct node* node = new struct node;
	node->data = data;
	node->left = NULL;
	node->right = NULL;
	return node;
}

void insert(struct node** rootRef, int data){
	if(*rootRef == NULL) {
		*rootRef = newNode(data);
	}else{
		if(data <= (*rootRef)->data){
			insert( &((*rootRef)->left), data);
		}else{
			insert( &((*rootRef)->right), data);
		}
	}

}

int size(struct node* root){
	if(root == NULL) return 0;
	return ( size(root->left)  + size(root->right) +1);
}

void printTreeInOrder(struct node* root){
	if(root == NULL) return;
	printTreeInOrder(root->left);
	cout << root->data << " ";
	printTreeInOrder(root->right);
}

void printTreePreOrder(struct node* root){
	if(root == NULL) return;
	cout << root->data << " ";
	printTreePreOrder(root->left);
	printTreePreOrder(root->right);
}

void printTreePostOrder(struct node* root){
	if(root == NULL) return;
	printTreePostOrder(root->left);
	printTreePostOrder(root->right);
	cout << root->data << " ";
}

int maxDepth(struct node* root){
	if(root == NULL) return 0;

	int lheight = maxDepth(root->left);
	int rheight = maxDepth(root->right);

	if(lheight > rheight){
		return (lheight + 1);
	}else{
		return (rheight + 1);
	}
}


bool lookup(struct node* root, int target){

	if(root == NULL) return false;

	if(root->data == target) return true;

	if(root->data > target){
		return lookup(root->left, target);
	}else{
		return lookup(root->right, target);
	}

}
//works with at least one node
int findMaxValue(struct node* root){
	if(root->right == NULL) return root->data;
    return findMaxValue(root->right);
}

int findMaxValueLoop(struct node* root){
	if(root->right == NULL) return root->data;
	struct node* temp = root;

	while(temp->right != NULL){
		temp = temp->right;
	}
	return temp->data;
}

int findMinValue(struct node* root){
	if(root->left == NULL) return root->data;
    return findMinValue(root->left);
}

struct node* findMin(struct node* root){
	while(root->left != NULL){
		root = root->left;
	}
	return root;
}

struct node* deleteNode(struct node* root, int target){
	if(root == NULL) return root;

	if(target < root->data){
		root->left = deleteNode(root->left, target);
	}else if(target > root->data){
		root->right = deleteNode(root->right, target);
	}else{  //found it!
		//Case 1: No child.
		if(root->left == NULL && root->right == NULL){
			delete root;
			return NULL;
		}
		//Case 2: One child.
		else if(root->left == NULL){  //right child
			struct node* temp = root->right;
			delete root;
			return temp;
		}else if(root->right == NULL){  // left child
			struct node* temp = root->left;
			delete root;
			return temp;
		}
		//Case 3: Two children.
		else{
			struct node* temp = findMin(root);
			root->data = temp->data;
			root->right = deleteNode(root->right, temp->data);

		}
	}
	return root;
}

//Function to find the kth largest element
void kthLargestUtil(struct node* root, int& k, int& result) {
    if (root == NULL || k <= 0)
        return;
    
    kthLargestUtil(root->right, k, result);
    k--;
    if (k == 0) {
        result = root->data;
        return;
    }
    kthLargestUtil(root->left, k, result);
}

int kthLargestElement(struct node* root, int k) {
    int result = -1;
    kthLargestUtil(root, k, result);
    return result;
}

//Function to delete all nodes and deallocate memory
void deleteTree(struct node* &root) {
    if (root == NULL)
        return;
    deleteTree(root->left);
    deleteTree(root->right);
    delete root;
    root = NULL;
}

int main() {
	struct node* root = NULL;
	insert(&root, 41);
	insert(&root, 20);
	insert(&root, 11);
	insert(&root, 29);
	insert(&root, 32);
	insert(&root, 65);
	insert(&root, 70);
	cout << "In-order: " ;
	printTreeInOrder(root);
	cout << endl;
	cout << "Pre-order: " ;
	printTreePreOrder(root);
	cout << endl;
	cout << "Post-order: " ;
	printTreePostOrder(root);
	cout << endl;
	cout << "Size: " << size(root) << endl;
	cout << "Max depth: " << maxDepth(root) << endl;
	cout << "Lookup 15: " << lookup(root, 15) << endl;
	cout << "Lookup 65: " << lookup(root, 65) << endl;
	cout << "Find max: "  << findMaxValueLoop(root) << endl;
	cout << "Find min: "  << findMinValue(root) << endl;
	deleteNode(root, 20);
	cout << "Pre-order: " ;
		printTreePreOrder(root);
	cout << endl;

	cout << "Kth largest element (k=2): " << kthLargestElement(root, 2) << endl;
	deleteTree(root);
	cout << "Tree deleted." << endl;

	return 0;
}

