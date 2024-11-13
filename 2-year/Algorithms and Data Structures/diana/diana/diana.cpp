#include <iostream>
#include <vector>
#include <fstream>
#include <sstream>
#include <algorithm>

using namespace std;

int maxPath;
int maxElem;

typedef struct tree_element {
    int value;
    struct tree_element* left;
    struct tree_element* right;
    int height;
} tree_element;

tree_element* create_tree_element(int i) {
    tree_element* elem = new tree_element;
    elem->value = i;
    elem->left = NULL;
    elem->right = NULL;
    return elem;
}

void insert_into_tree(tree_element* root, tree_element* elem) {
    if (elem->value == root->value) {
        return;
    }
    if (elem->value < root->value) {
        if (root->left == NULL) {
            root->left = elem;
        }
        else {
            insert_into_tree(root->left, elem);
        }
    }
    else {
        if (root->right == NULL) {
            root->right = elem;
        }
        else {
            insert_into_tree(root->right, elem);
        }
    }
}

tree_element* find_min(tree_element* root) {
    while (root->left != NULL) {
        root = root->left;
    }
    return root;
}

tree_element* delete_node(tree_element* root, int value) {
    if (root == NULL) {
        return root;
    }

    if (value < root->value) {
        root->left = delete_node(root->left, value);
    }
    else if (value > root->value) {
        root->right = delete_node(root->right, value);
    }
    else {
        if (root->left != NULL && root->right != NULL) {
            tree_element* temp = find_min(root->right);
            root->value = temp->value;
            root->right = delete_node(root->right, temp->value);
        }
        else {
            tree_element* temp = root;
            if (root->left == NULL) {
                root = root->right;
            }
            else if (root->right == NULL) {
                root = root->left;
            }
            delete temp;
        }
    }
    return root;
}

void findHeight(tree_element* node) {
    if (node == NULL) return;
    findHeight(node->left);
    findHeight(node->right);
    int leftHeight, rightHeight;
    if (node->left == NULL) leftHeight = -1;
    else leftHeight = node->left->height;
    
    if (node->right == NULL) rightHeight = -1;
    else rightHeight = node->right->height;

    node->height = max(leftHeight, rightHeight) + 1;
    if (leftHeight + rightHeight >= maxPath) {
        maxPath = leftHeight + rightHeight;
        maxElem = node->value;
    }
}

void print_tree_preorder(tree_element* cur_elem, ofstream& out) {
    if (cur_elem == NULL) {
        return;
    }
    out << cur_elem->value << endl;
    print_tree_preorder(cur_elem->left, out);
    print_tree_preorder(cur_elem->right, out);
}


int main() {
    maxPath = -2;
    maxElem = -1;
    int key_to_delete;
    vector<int> keys;
    ifstream in("input.txt");

    int key;
    while (in >> key) {
        keys.push_back(key);
    }

    if (keys.empty()) {
        return 0;
    }

    tree_element* root = create_tree_element(keys[0]);
    for (size_t i = 1; i < keys.size(); i++) {
        tree_element* el = create_tree_element(keys[i]);
        insert_into_tree(root, el);
    }


    ofstream out("output.txt");
    if (!out.is_open()) {
        cerr << "Не удалось открыть файл для записи." << endl;
        return 1;
    }

    findHeight(root);
    root = delete_node(root, maxElem);


    print_tree_preorder(root, out);

    out.close();
    return 0;
}
