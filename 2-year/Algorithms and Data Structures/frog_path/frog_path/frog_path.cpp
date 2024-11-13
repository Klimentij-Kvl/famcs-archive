#include <iostream>
#include <string>
#include <algorithm>

using namespace std;

int n;
int* arr;
long* a;

long F(int i) {
    if (i > 0 && i < n + 1) {
        if (i == 1) return arr[0];


        if (a[i - 1] == -1) {
            a[i - 1] = max(F(i - 2), F(i - 3)) + arr[i - 1];
        }

        return a[i - 1];
    }

    return -1;
}

int main()
{
    cin >> n;
    

    arr = new int[n];
    a = new long[n];
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
        a[i] = -1;
    }
    if (n < 3) {
        cout << -1;
        return 0;
    }

    a[0] = arr[0]; a[1] = -2;

    long x = F(n);
    cout << x << "\n";

    string s=to_string(n);
    long y=arr[n-1];
    int i = n-1;
    while(i > 1){
        if (a[i - 2] + y == x) {
            s = to_string(i - 1) + " " + s;
            y += arr[i-2];
            i -= 2;
        }
        else if (a[i - 3] + y == x) {
            s = to_string(i - 2) + " " + s;
            y += arr[i-3];
            i -= 3;
        }
    }
    cout << s;
}

