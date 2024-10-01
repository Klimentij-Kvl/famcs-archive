package main;

public class task3 {
    int[][] main(int a, int b, int[][] m){
        int max = m[0][0];
        int maxI = 0;
        int maxJ = 0;
        for(int i = 0; i < a; i++){
            for(int j = 0; j < b; j++){
                if(m[i][j] > max){
                    max = m[i][j];
                    maxI = i;
                    maxJ = j;
                }
            }
        }

        int buff;
        for(int i = 0; i < a; i++){
            buff = m[i][0];
            m[i][0] = m[i][maxJ];
            m[i][maxJ] = buff;
        }
        for(int i = 0; i < a; i++){
            buff = m[0][i];
            m[0][i] = m[maxI][i];
            m[maxI][i] = buff;
        }

        return m;
    }
}
