#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

class tree {
private:
    vector<long long> t;
    vector<long long> a;
    int n;

    void doBuild(int v, int tl, int tr) {
        if (tr - tl == 1)
            t[v] = a[tl];
        else {
            int m = (tl + tr) / 2;
            doBuild(2 * v, tl, m);
            doBuild(2 * v + 1, m, tr);
            t[v] = t[2 * v] + t[2 * v + 1];
        }
    }

    void doAdd(int v, int tl, int tr, int pos, long long x) {
        if (tr - tl == 1) {
            t[v] += x;
            return;
        }
        int m = (tl + tr) / 2;
        if (pos < m)
            doAdd(2 * v, tl, m, pos, x);
        else
            doAdd(2 * v + 1, m, tr, pos, x);
        t[v] = t[2 * v] + t[2 * v + 1];
    }

    long long doFindSum(int v, int tl, int tr, int l, int r) {
        if (l == tl && r == tr) return t[v];
        int m = (tl + tr) / 2;
        if (r <= m) return doFindSum(2 * v, tl, m, l, r);
        if (l >= m) return doFindSum(2 * v + 1, m, tr, l, r);
        return doFindSum(2 * v, tl, m, l, m) + doFindSum(2 * v + 1, m, tr, m, r);
    }
public:
    tree(){}
    tree(int n) {
        t.resize(4*n);
        a.resize(n);
        this->n = n;
        fill(t.begin(), t.end(), 0);
        for (int i = 0; i < n; i++) {
            cin >> a[i];
        }
    }

    void build() {
        doBuild(1, 0, n);
    }

    void add(int pos, long long x) {
        doAdd(1, 0, n, pos, x);
    }

    long long findSum(int l, int r) {
        return doFindSum(1, 0, n, l, r);
    }

    void printTree() {
        for (int i = 0; i < 4*n; i++) cout << t[i] << " ";
    }
};

int main()
{
    int n; cin >> n;
    tree t(n);
    t.build();
    int q;
    cin >> q;
    string s; int l;
    long long r;
    for (int i = 0; i < q; i++) {
        cin >> s >> l >> r;
        if (s == "Add") t.add(l, r);
        else cout << t.findSum(l, r) << endl;
    }
}