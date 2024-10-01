package main;

public class task1 {
        public int Main(int a, int b, int[][] m) {
            int ans = 0, max = 0, c = 0;

            for (int i = 0; i < a; i++) {
                for (int j = 0; j < b - 1; j++) {
                    while (j < b - 1 && m[i][j] == m[i][j + 1]) {
                        c++;
                        j++;
                    }
                    c++;
                    if (c > max) {
                        max = c;
                        ans = i;
                    }
                }
            }

            return ans;
        }
}
