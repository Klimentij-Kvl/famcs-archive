package main;

public class task4 {
    double Main(int a, int[][] m){
        int buff = 1;
        double ans = 1;
        int c,d;
        for(int i =0; i < a-1; i++) {
            for (int j = i+1; j < a; j++) {
                c = m[j][i];
                if (c != 0) {
                    buff *= m[i][i];
                    for (int k = i; k < a; k++) {
                        m[j][k] = m[j][k] * m[i][i] - m[i][k] * c;
                    }
                }
            }
        }

        for(int i = 0; i < a; i++){
            for(int j = 0; j < a; j++){
                System.out.printf("%d ", m[i][j]);
            }
            System.out.println();
        }

        for(int i = 0; i < a; i++){
            ans *= m[i][i];
        }

        ans /= buff;

        return ans;
    }
}
