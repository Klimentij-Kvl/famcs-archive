// 0.6 polyndrom.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <fstream>
#include <string>
#include <algorithm>

using namespace std;

int main()
{
    ifstream cin("input.txt");
    ofstream cout("output.txt");

    string s;
    cin >> s;

    int n = s.length();
    int** m;
    m = new int*[n];
    for (int i = 0; i < n; i++) {
        m[i] = new int[n];
        for (int j = 0; j < n; j++) m[i][j] = 0;
    }

    for (int i = 0; i < n-1; i++) {
        m[i][i] = 1;
        if (s[i] == s[i + 1]) m[i][i + 1] = 2;
        else m[i][i + 1] = 1;
    }
    m[n - 1][n - 1] = 1;

    for (int i = 2; i < n; i++) {
        for (int j = 0; j < n-i; j++) {
            if (s[j] == s[i + j]) m[j][i + j] = m[j + 1][i + j - 1] + 2;
            else m[j][i + j] = max(m[j+1][i+j], m[j][i+j-1]);
        }
    }

    /*for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) cout << m[i][j] << " ";
        cout << endl;
    }*/

    cout << m[0][n - 1] << endl;

    string ans="";
    int i = 0; int j = n-1;
    while (m[i][j] > 1) {
        if (s[i] == s[j]) {
            ans = ans + s[i];
            i++;
            j--;
        }
        else if (m[i+1][j] > m[i][j - 1]) i++;
        else j--;
    }
    string ansr = ans;
    reverse(ansr.begin(),ansr.end());
    if (m[i][j] == 1)
        cout << ans + s[i] + ansr;
    else
        cout << ans + ansr;
}
