// 0.1.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>

using namespace std;

bool binFinder(int n, int *a, int key) {
    int start=0, end=n, point;
    while (end > start) {
        point = (end + start) / 2;
        if (a[point] == key) {
            return 1;
        }

        if (a[point] < key) {
            start = point+1;
        }
        else {
            end = point;
        }
    }
    return 0;
}

int leftFinder(int n, int *a, int key) {
    int start = 0, end = n, point;
    while (end > start) {
        point = (start + end) / 2;
        if (a[point] >= key) {
            end = point;
        }
        else {
            start = point + 1;
        }
    }
    return start;
}

int lowerBound(int n, int* a, int key) {
    int start = 0, end = n, point;
    while (end > start) {
        point = (start + end) / 2;
        if (a[point] > key) {
            end = point;
        }
        else {
            start = point + 1;
        }
    }
    return start;
}

int main()
{
    int* a, * b;
    int n, k, x;

    cin >> n;
    a = new int[n];
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }

    cin >> k;
    for (int i = 0; i < k; i++) {
        cin >> x;
        cout << binFinder(n, a, x) << " " << leftFinder(n,a,x) << " " << lowerBound(n,a,x) << endl;
    }
}
