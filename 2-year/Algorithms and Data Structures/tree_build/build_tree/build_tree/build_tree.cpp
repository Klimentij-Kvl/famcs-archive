//#include <iostream>
#include <fstream>
#include <string>
#include <algorithm>
#include <vector>

using namespace std;

ofstream cout;

vector<int> answers;

struct node {
    int data;

    int Rcount;
    int Lcount;

    int Rheight;
    int Lheight;
    int height;

    node* left;
    node* right;
};

node* addNode(node* Node, int a) {
        if (Node == NULL) {
            Node = new node;
            Node->data = a;
            Node->Rcount = 0;
            Node->Lcount = 0;
            Node->Rheight = -1;
            Node->Lheight = -1;
            Node->height = 0;
            Node->left = NULL;
            Node->right = NULL;
        }
        else {
            if (a == Node->data)
                return Node;
            if (a < Node->data) {
                Node->left = addNode(Node->left, a);
                Node->Lcount++;
                Node->Lheight = Node->left->height;
            }
            else if (a > Node->data) {
                Node->right = addNode(Node->right, a);
                Node->Rcount++;
                Node->Rheight = Node->right->height;
            }

            Node->height = max(Node->Lheight, Node->Rheight)+1;
        }
        return Node;
        
}

node* findMinElem(node* Node) {
    if (Node->left == NULL) {
        return Node;
    }
    return findMinElem(Node->left);
}

node* deleteNode(node* Node, int x) {
    if (Node->data == x) {
        if (Node->left == NULL && Node->right == NULL) {
            return NULL;
        }
        else if (Node->left == NULL) {
            return Node->right;
        }
        else if (Node->right == NULL) {
            return Node->left;
        }
        node* minNode = findMinElem(Node->right);
        Node->data = minNode->data;
        Node->right = deleteNode(Node->right, minNode->data);
    }
    else if (Node->data > x)
        Node->left = deleteNode(Node->left, x);
    else if (Node->data < x)
        Node->right = deleteNode(Node->right, x);

    return Node;
}

void findAns(node* v){
    if (v != NULL) {

        if (v->Rheight != v->Lheight && v->Lcount == v->Rcount)
            answers.push_back(v->data);

        findAns(v->left);
        findAns(v->right);
    }
}

void PreOrderTraversal(node* v) {
    if (v != NULL) {
        /*cout << v->data << " Rcount:" << v->Rcount << " Lcount:" << v->Lcount
            << " Rheight:" << v->Rheight << " Lheight:" << v->Lheight 
            << " height:" << v->height << endl;*/
        cout << v->data << endl;
        PreOrderTraversal(v->left);
        PreOrderTraversal(v->right);
    }
}

int main()
{
    ifstream cin;
    cin.open("input.txt");
    cout.open("output.txt");
    if (!cin.is_open()) {
        return 2;
    }

    node* root = NULL;
    for (int m; cin >> m; ) {
        root = addNode(root, m);
    }
    
    findAns(root);

    root = deleteNode(root, *min_element(answers.begin(), answers.end()));

    PreOrderTraversal(root);

    //for (int i = 0; i < answers.size(); i++) cout << answers[i] << " ";

    cin.close();
    cout.close();
    return 0;
}