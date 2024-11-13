// 0.3  ones(2).cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include <cmath>

const long long p = 1000000007;

using namespace std;
long long F(int b, int n) {
    if (n == 0)		    /// ограничение 2
        return 1;
    if (n == 1)		    /// ограничение 1
        return b;
    unsigned long long t = F(b, n >> 1);/// t = F(n / 2);	  
    if ((n & 1) == 0)       /// n % 2 == 0
        return  (t * t) % p;	   /// рекурс. ф-я 1
    return (((t * t)%p) * b) % p;   /// t * t *2 ///рекурс. ф-я 2
}


int main()
{
    int n, k;
    cin >> n >> k;
    unsigned long long c = 1;


    unsigned long long x=1, y=1;
    int  k1 = k;
    while (k > 0) {
        c = (c*(n-k+1)*x) % p;
        y = (y * F(k, p - 2)) % p;
        k--;
    }
    
    
    /*while (k > 0) {
        x = (x * (F(k,p-2)%p)) % p;
        x %= p;
        k--;
    }*/

    cout << (c*y)%p;
}