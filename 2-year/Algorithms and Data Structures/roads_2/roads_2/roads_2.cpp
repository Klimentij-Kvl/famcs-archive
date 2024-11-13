// roads_1.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include <fstream>
#include <vector>
#include <map>

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
    //ifstream cin("input.txt");
    //ofstream cout("output.txt");
    int n, m, q;
    cin >> n >> m >> q;

    vector<int> fir(m);
    vector<int> sec(m);
    vector<int> arr(q);
    map<int, bool> Map;

    for (int i = 0; i < m; i++) {
        cin >> fir[i] >> sec[i];
        fir[i]--;
        sec[i]--;
    }

    for (int i = 0; i < q; i++) {
        cin >> arr[i];
        arr[i]--;
        Map[arr[i]] = true;   
    }
    DSU dsu(n);
    for (int i = 0; i < m; i++) {
        if (Map.count(i) == 0) {
            dsu.Union(fir[i], sec[i]);
        }
    }
    
    string s = "";
    if (dsu.ConnectionNumber() == 1) {
        s = "1" + s;
    }
    else s = "0" + s;
    for (int i = q-1; i > 0; i--) {
        dsu.Union(fir[arr[i]], sec[arr[i]]);
        if (dsu.ConnectionNumber() == 1) {
            s = "1" + s;
        }
        else s = "0" + s;
    }
    cout << s;
}