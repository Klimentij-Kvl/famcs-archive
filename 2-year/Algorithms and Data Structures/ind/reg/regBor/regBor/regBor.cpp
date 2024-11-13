//#include <iostream>
#include <fstream>
#include <string>

using namespace std;

ofstream cout("output.txt");

struct node {
    int data;
    node* left;
    node* right;
    node() {
        data = 0;
        left = NULL;
        right = NULL;
    }
    node(int a) {
        data = a;
        left = NULL;
        right = NULL;
    }
};

void PreOrderTraversal(node* v) {
    if (v != NULL) {
        cout << v->data << endl;
        PreOrderTraversal(v->left);
        PreOrderTraversal(v->right);
    }
}

int main()
{
    ifstream in("input.txt");
    if (!in.is_open()) {
        return 2;
    }
    
    int n, m;
    //cin >> n;
    node* head = new node();
    node* root = head;
    in >> head->data;

    while (!in.eof()) {
        in >> m;
        head = root;
        while (true) {
            if (m > head->data) {
                if (head->right == NULL) {
                    head->right = new node(m);
                    break;
                }
                head = head->right;

            }
            else if (m < head->data) {
                if (head->left == NULL) {
                    head->left = new node(m);
                    break;
                }
                head = head->left;
            }
        }
    }
    PreOrderTraversal(root);

    return 0;
}