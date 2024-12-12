#include <iostream>
#include <list>
#include <vector>

using namespace std;

//ifstream cin("input.txt");
//ofstream cout("output.txt");

class Solution {
private:
    list<int>* g;
    list<int>* rg;
    list<int>* c;
    list<int>* rc;
    int* terminals;
    int n;
    bool* visited;
    list<int> ordered;
    int* component;
    int components;
    
    int* toCond;
    int minTerminal;
    int index;
public:
    Solution(){}
    Solution(int n) {
        g = new list<int>[n];
        rg = new list<int>[n];
        terminals = new int[n];
        visited = new bool[n];
        component = new int[n];
        toCond = new int[n];
        for (int i = 0; i < n; i++)
            visited[i] = false;
        this->n = n;
        components = 0;
        index = 0;
        minTerminal = 2000;
    }

    void readGraph() {
        for (int i = 0; i < n; i++) {
            cin >> terminals[i];
        }

        int a, b;
        cin >> a >> b;
        for (; a > 0 && b > 0; cin >> a >> b) {
            g[a - 1].push_back(b - 1);
            rg[b - 1].push_back(a - 1);
        }
    }

    void writeGraph() {
        cout << "\ngraph:" << endl;
        for (int i = 0; i < n; i++) {
            cout << i << ": ";
            for (int j : g[i])
                cout << j << " ";
            cout << endl;
        }

        cout << "\nrgraph:" << endl;
        for (int i = 0; i < n; i++) {
            cout << i << ": ";
            for (int j : rg[i])
                cout << j << " ";
            cout << endl;
        }

        cout << "\ncomponents:" << endl;
        for (int i = 0; i < n; i++) {
            cout << component[i] << " ";
        }

        cout << "\ntoCond:\n";
        for (int i = 0; i < components; i++) {
            cout << toCond[i] << " ";
        }

        cout << "\n\nc:\n";
        for (int i = 0; i < components; i++) {
            cout << i << ": ";
            for (int j : c[i]) {
                cout << j << " ";
            }
            cout << endl;
        }
        cout << "\n\nrc:\n";
        for (int i = 0; i < components; i++) {
            cout << i << ": ";
            for (int j : rc[i]) {
                cout << j << " ";
            }
            cout << endl;
        }
    }

    void dfs1(int v) {
        visited[v] = true;
        for (int u : g[v])
            if (!visited[u])
                dfs1(u);
        ordered.push_front(v);
    }

    void dfs2(int v) {
        visited[v] = true;
        component[v] = components;
        if (minTerminal > terminals[v]) {
            minTerminal = terminals[v];
            index = v;
        }
        for (int u : rg[v])
            if (!visited[u])
                dfs2(u);
    }

    void strongly_connected() {
        for (int v = 0; v < n; v++)
            if (!visited[v])
                dfs1(v);

        for (int v = 0; v < n; v++)
            visited[v] = false;

        for (int v : ordered) {
            if (!visited[v]) {
                minTerminal = 2000;
                dfs2(v);
                toCond[components] = index;
                components++;
            }
        }

        c = new list<int>[components];
        rc = new list<int>[components];
        for (int i = 0; i < n; i++) {
            for (int j : g[i]) {
                if (component[i] != component[j]) {
                    c[component[i]].push_back(component[j]);

                    rc[component[j]].push_back(component[i]);
                }
            }
        }
        int ans = 0;
        vector<int> a;
        for (int i = 0; i < components; i++) {
            if (rc[i].empty()) {
                ans++;
                a.push_back(toCond[i]);
            }
        }
        cout << ans << endl;
        for (int i : a) cout << i+1 << " ";
    }
};

/*
10
1 1 1 1 1 1 1 1 1 1
2 1
1 4
4 3
3 2
2 6
1 5
4 5
3 7
8 3
9 6
10 4

7
1 1 1 1 1 1 1
1 4
4 3
3 2
2 1
5 4
6 4
6 5
5 7
7 6
*/

int main()
{
    int n;
    cin >> n;
    Solution sol(n);
    sol.readGraph();
    sol.strongly_connected();
    //sol.writeGraph();
}
