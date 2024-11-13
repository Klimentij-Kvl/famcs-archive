// 0.7 lis.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <fstream>

using namespace std;

int UpperBound(int key, int* a, int n) {
    int l = 0, r = n-1;
    int m;
    while (l < r) {
        m = (l + r) / 2;
        if (key < a[m])
            r = m;
        else
            l = m + 1;
    }
    return l;
}

int main()
{
    ifstream cin("input.txt");
    ofstream cout("output.txt");

    int  n, m;
    cin >> n;

    int* a;
    a = new int[n];
    cin >> a[0];

    int k = 0, x;
    for (int i = 1; i < n; i++) {
        cin >> m;
        if (m > a[k]) {
            k++;
            a[k] = m;
        }
        else {
            x = UpperBound(m, a, k+1);
            if(a[x-1] != m)a[x] = m;
        }
    }

    cout << k+1  << endl;
    for (int i = 0; i < n; i++) cout << a[i] << " ";
}
