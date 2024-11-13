#include <iostream>

using namespace std;

int main()
{
    int* a, * b;
    int n, k;
    cin >> n >> k;
    a = new int[k + 1];
    b = new int[k + 1];
    for (int i = 0; i <= n; i++) {
        for (int j = 0; j <= k; j++) {
            if (j == 0) b[j] = 1;
            else if (j == i) b[j] = 1;
            else b[j] = (a[j] + a[j - 1]) % 1000000007;
        }

        for (int j = 0; j <= k; j++) a[j] = b[j];

    }
    cout << a[k];
}