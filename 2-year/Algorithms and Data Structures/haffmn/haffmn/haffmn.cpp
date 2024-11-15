#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <limits>

using namespace std;

int main()
{
	//ifstream cin("huffman.in");
	//ofstream cout("huffman.out");
	int n;
	cin >> n;
	vector<int>arr1(n);
	vector<long long>arr2(n);
	long long s;
	long long su = 0;
	long long l, r;

	for (int i = 0; i < n; i++) {
		cin >> arr1[i];
	}
	int i = 0, j = 0;
	for (int k = 0; k < n - 1; k++) {

		if (i < n && (j == k || arr1[i] <= arr2[j])) {
			l = arr1[i];
			i++;
		}
		else {
			l = arr2[j];
			j++;
		}

		if (i < n && (j == k || arr1[i] <= arr2[j])) {
			r = arr1[i];
			i++;
		}
		else {
			r = arr2[j];
			j++;
		}


		s = l + r;
		su += s;
		arr2[k] = s;
	}
	cout << su;
}