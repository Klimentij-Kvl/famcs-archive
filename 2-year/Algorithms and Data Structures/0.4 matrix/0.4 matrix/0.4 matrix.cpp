// 0.4 matrix.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <fstream>

using namespace std;

int main()
{
    int s, x=0;
    ifstream cin("input.txt");
    ofstream cout("output.txt");
    cin >> s;
    int** a, ** m;
    a = new int*[s];
    m = new int* [s];
    for (int i = 0; i < s; i++) {
        m[i] = new int[s];
        //for (int j = 0; j < s; j++) m[i][j] = 0;
        a[i] = new int[2];
        cin >> a[i][0] >> a[i][1];
    }

    for (int i = 0; i < s; i++) {
        

        m[i][i] = 0;
        for (int j = i-1; j >= 0; j--) {
            if (j == i - 1) m[j][i] = a[j][0] * a[j][1] * a[i][1];
            else {
                m[j][i] = m[j][j] + m[j + 1][i] + a[j][0] * a[j][1] * a[i][1];
                for (int k = j+1; k < i; k++) {
                    x = m[j][k] + m[k+1][i] + a[j][0] * a[k][1] * a[i][1];
                    if (m[j][i] > x) m[j][i] = x;
                }
            }
        }
    }

    /*for (int i = 0; i < s; i++) {
        for (int j = 0; j < s; j++)
            cout << m[i][j] << " ";
        cout << endl;
    }*/
    cout << m[0][s - 1];
}
