// roads_1.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include <fstream>
#include <vector>

using namespace std;

class DSU {
private:
    vector<int> Parent;
    int connectionNumber;
public:
    DSU(int n) {
        for (int i = 0; i < n; i++) {
            Parent.push_back(-1);
        }
        connectionNumber = n;
    }

    int FindSet(int x) {
        if (Parent[x] < 0) return x;
        Parent[x] = FindSet(Parent[x]);
        return Parent[x];
    }

    void Union(int x, int y) {
        x = FindSet(x);
        y = FindSet(y);
        if (x == y) return;
        if (Parent[x] > Parent[y]) {
            int a = x;
            x = y;
            y = a;
        }
        Parent[x] += Parent[y];
        Parent[y] = x;
        connectionNumber--;
    }

    int ConnectionNumber() {
        return connectionNumber;
    }
};

int main()
{
    ifstream cin("input.txt");
    ofstream cout("output.txt");
    int n, q;
    cin >> n >> q;
    DSU dsu(n);
    int  a, b;
    for (int i = 0; i < q; i++) {
        cin >> a >> b;
        dsu.Union(a - 1, b - 1);
        cout << dsu.ConnectionNumber() << endl;
    }
}