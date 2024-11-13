// LCS.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include <algorithm>
#include <string>

using namespace std;

int main()
{
	int a;
	int** m;
	int* A, * B;
	cin >> a;
	m = new int* [a+1];

	for (int i = 0; i < a + 1; i++) {
		m[i] = new int[a + 1];
		m[i][0] = 0;
	}

	for (int i = 0; i < a + 1; i++) m[0][i] = 0;

	A = new int[a]; B = new int[a];
	for (int i = 0; i < a; i++) {
		cin >> A[i];
	}

	for (int i = 0; i < a; i++) {
		cin >> B[i];
	}

	for (int i = 1; i <= a; i++) {
		for (int j = 1; j <= a; j++) {
			if (A[i-1] == B[j-1])
				m[i][j] = m[i - 1][j - 1] + 1;
			else
				m[i][j] = max(m[i - 1][j], m[i][j - 1]);
		}
	}

	/*for (int i = 0; i < a + 1; i++) {
	
		for (int j = 0; j < a + 1; j++)
			cout << m[i][j] << " ";
		cout << endl;
	}*/
	cout << m[a][a] << endl;

	int i = a, j = a;
	string s1="", s2 = "";
	while (m[i][j] != 0) {
		if (A[i - 1] == B[j - 1]) {
			s1 = to_string(i - 1) + " " + s1;
			s2 = to_string(j - 1) + " " + s2;
			i--; j--;
		}
		else if (m[i][j] == m[i - 1][j]) {
			i--;
		}
		else j--;
	}
	cout << s1 << "\n" << s2;
	/*for (int i = 0; i < a + 1; i++) {

		for (int j = 0; j < a + 1; j++)
			cout << m[i][j] << " ";
		cout << endl;
	}*/
}

// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

// Tips for Getting Started: 
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file
