// tree.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <fstream>
#include <algorithm>
#include <vector>

using namespace std;

ofstream cout;

class Tree {
private:
    struct node {
        int data;
        node* right;
        node* left;
        node(int x) {
            data = x;
            right = NULL;
            left = NULL;
            children = 1;
            height = 0;
            isAnswer = false;
        }

        int children;
        int height;
        bool isAnswer;
    };

    node* root;
    vector<int> answers;

    void _showNode(node* v) {
        if (v != NULL) {
            cout << v->data/* << " " << v->height << " " << v->children*/ << endl;
            _showNode(v->left);
            _showNode(v->right);
        }
    }

    node* _findMin(node* v) {
        if (v->left != NULL) return _findMin(v->left);
        return v;
    }

    node* _deleteNode(node* Node, int x) {
        if (Node->data == x) {
            if (Node->left == NULL && Node->right == NULL) return NULL;
            if (Node->left == NULL) return Node->right;
            if (Node->right == NULL) return Node->left;

            node* MinNode = _findMin(Node->right);
            Node->data = MinNode->data;
            Node->right = _deleteNode(Node->right, MinNode->data);

            return Node;
        }
        
        if (Node->data > x) {
            if (Node->left == NULL) return Node;
            Node->left = _deleteNode(Node->left, x);
            return Node;
        }

        if (Node->data < x) {
            if (Node->right == NULL) return Node;
            Node->right = _deleteNode(Node->right, x);
            return Node;
        }
    }

    void _editTree(node* Node) {
        if (Node != NULL) {
            _editTree(Node->left);
            _editTree(Node->right);

            int hL, hR, cL, cR;
            if (Node->left == NULL) {
                hL = -1; cL = 0;
            }
            else {
                hL = Node->left->height;
                cL = Node->left->children;
            }

            if (Node->right == NULL) {
                hR = -1; cR = 0;
            }
            else {
                hR = Node->right->height;
                cR = Node->right->children;
            }

            Node->children = cL + cR + 1;
            Node->height = max(hL, hR) + 1;
            if (hL != hR && cL == cR) answers.push_back(Node->data);
        }
    }
public:
    Tree() {
        root = NULL;
    };

    void addNode(int x) {
        node** head = &root;
        while (*head != NULL) {
            node* cur = *head;
            if (cur->data > x) {
                head = &cur->left;
            }
            else if (cur->data < x) {
                head = &cur->right;
            }
            else {
                return;
            }
        }

        *head = new node(x);
    }

    void deleteNode(int x) {
        if (root == NULL) return;
        root = _deleteNode(root, x);
    }

    int findAns() {
        _editTree(root);
        if (answers.size() % 2 == 0) return -5;
        sort(answers.begin(), answers.end());
        return answers[answers.size() / 2];
    }

    void show() {
        _showNode(root);
    }
};

int main()
{
    cout.open("output.txt");
    ifstream cin("input.txt");
    Tree tree;
    for (int m; cin >> m; tree.addNode(m));

    int n = tree.findAns();
    if (n != -5) tree.deleteNode(n);
    tree.show();
   
    cout.close();
    cin.close();

}
