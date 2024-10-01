package main;

public class task2 {
    public int Main(int a, int b, int[][] m){
        int ans = 0;

        if(m[0][0] < m[0][1] && m[0][0] < m[1][0]){
            ans++;
        }
        if(m[a-1][0] < m[a-1][1] && m[a-1][0] < m[a-2][0]){
            ans++;
        }
        if(m[0][b-1] < m[0][b-2] && m[0][b-1] < m[a-1][b-1]){
            ans++;
        }
        if(m[a-1][b-1] < m[a-1][b-2] && m[a-1][b-1] < m[a-2][b-1]){
            ans++;
        }


        for(int i = 1; i < a-1; i++){
            if(m[i][0] < m[i][1] && m[i][0] < m[i-1][0] && m[i][0] < m[i+1][0]){
                ans++;
            }
            if(m[i][b-1] < m[i][b-2] && m[i][b-1] < m[i-1][b-1] && m[i][b-1] < m[i+1][b-1]){
                ans++;
            }
        }
        for(int i = 1; i < b-1; i++){
            if(m[0][i] < m[1][i] && m[0][i] < m[0][i-1] && m[0][i] < m[0][i+1]){
                ans++;
            }
            if(m[a-1][i] < m[a-2][i] && m[a-1][i] < m[a-1][i-1] && m[a-1][i] < m[a-1][i+1]){
                ans++;
            }
        }

        for(int i = 1; i < a-1; i++){
            for(int j = 1; j < b-1; j++){
                if(m[i][j] < m[i+1][j] && m[i][j] < m[i][j+1] &&
                        m[i][j] < m[i-1][j] && m[i][j] < m[i][j-1]){
                    ans++;
                }
            }
        }

        return ans;
    }
}
