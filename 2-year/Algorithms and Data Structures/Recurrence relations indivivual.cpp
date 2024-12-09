
#include <iostream>
#include <algorithm>
#include <vector>

using namespace std;

int main()
{
    int n, k, *arr, **m1, **m2;
    cin >> n;
    arr = new int[n];
    m1 = new int* [n];
    m2 = new int* [n];
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
        m1[i] = new int[n];
        m2[i] = new int[n];
    }
    for (int i = 0; i < n; i++) {
        m1[i][i] = arr[i];
        m2[i][i] = 0;
    }
    for (int i = 1; i < n; i++) {
        for (int j = 0; j < n - i; j++) {
            if (arr[j] + m2[i + j][j + 1] >= arr[i + j] + m2[i + j - 1][j]) {
                m1[i + j][j] = arr[j] + m2[i + j][j + 1];
                m2[i + j][j] = m1[i + j][j + 1];
            }
            else {
                m1[i + j][j] = arr[i + j] + m2[i + j - 1][j];
                m2[i + j][j] = m1[i + j - 1][j];
            }
        }
    }

    cout << m1[n - 1][0];
}