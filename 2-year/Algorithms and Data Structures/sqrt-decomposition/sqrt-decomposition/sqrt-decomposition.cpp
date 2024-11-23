#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>

using namespace std;

class Summatorr {
private:
    vector<long long> arr;
    vector<long long> blocks;
    int blocksSize;

public:
    Summatorr(){}

    Summatorr(int n) {
        blocksSize = floor(sqrt(n));
        arr.resize(n);
        blocks.resize(blocksSize+1);
        //for (int i = 0; i < blocksSize; i++) blocks[i] = 0;
        fill(blocks.begin(), blocks.end(), 0);
        for (int i = 0; i < n; i++) {
            cin >> arr[i];
            blocks[i / blocksSize] += arr[i];
        }
    }

    void add(int pos, long long x) {
        arr[pos] += x;
        blocks[pos / blocksSize] += x;
    }

    int findSum(int l, int r) {
        int bl = l / blocksSize;
        int br = r / blocksSize;
        long long s = 0;
        if (bl == br) {
            for (int i = l; i < r; i++)
                s += arr[i];
            return s;
        }

        for (int i = bl+1; i < br; i++) {
            s += blocks[i];
        }
        for (int i = l; i < (bl+1) * blocksSize; i++) {
            s += arr[i];
        }
        for (int i = br* blocksSize; i < r; i++) {
            s += arr[i];
        }

        return s;
    }
};

int main()
{
    int n, m;
    long long l, r;
    cin >> n;
    Summatorr rofl(n);
    cin >> m;
    string s;
    for (int i = 0; i < m; i++) {
        cin >> s >> l >> r;
        if (s == "Add") rofl.add(l, r);
        else cout << rofl.findSum(l, r) << endl;
    }
}
