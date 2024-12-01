#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <map>
#include <cstdlib>

using namespace std;

class Summatorr {
private:
    vector<int> arr;
    vector<int> blocks;
    int blocksSize;

public:
    Summatorr() {}

    Summatorr(int n) {
        n = n*3 +1;
        blocksSize = floor(sqrt(n));
        arr.resize(n);
        blocks.resize(blocksSize + 2);
        //for (int i = 0; i < blocksSize; i++) blocks[i] = 0;
        fill(arr.begin(), arr.end(), INT_MAX);
        fill(blocks.begin(), blocks.end(), INT_MAX);
    }

    void add(int pos, int x) {
        arr[pos] = x;
        blocks[pos / blocksSize] = min(blocks[pos / blocksSize], x);
    }

    int findMin(int r) {
        int mini = INT_MAX;
        for (int i = 0; i < r / blocksSize; i++) {
            mini = min(mini, blocks[i]);
        }

        for (int i = (r / blocksSize) * blocksSize + 1; i < r; i++) {
            mini = min(mini, arr[i]);
        }

        return mini;
    }
};

int comparator(const void *x1, const void *x2) {
    return (*(int*)x1 - *(int*)x2);
}

int main()
{
    int n, a, b;
    cin >> n;
    Summatorr rofl(n);
    int* arr = new int[n];
    map<int, int> connect;
    map<int, int> connect2;
    for (int i = 0; i < n; i++) {
        cin >> arr[i] >> a >> b;
        connect[arr[i]] = a;
        connect2[a] = b;
    }

    qsort(arr, n, sizeof(int), comparator);
    
    int s = 0, l, r;
    for (int i = 0; i < n; i++) {
        l = connect2[connect[arr[i]]];
        rofl.add(connect[arr[i]], l);
        r = rofl.findMin(connect[arr[i]]);
        if (l < r) {
            s++;
        }
    }

    cout << s;
    /*
    8
    2 9 1 9 6 7 5 2
    */
}