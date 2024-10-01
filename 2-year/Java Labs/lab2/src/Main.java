import java.util.Scanner;

class task1 {
    public int Main() {
        int[][] matrix;
        int a,b;
        Scanner in = new Scanner(System.in);

        System.out.println("Type a and b - size of your matrix: ");
        a = in.nextInt(); b = in.nextInt();
        matrix = new int[a][b];

        System.out.println("Type your matrix: ");
        for(int i = 0; i < a; i++) {
            for (int j = 0; j < b; j++) {
                matrix[i][j] = in.nextInt();
            }
        }

        int ans = 0, max = 0, c = 0;

        for(int i = 0; i < a; i++){
            for(int j = 0; j < b-1; j++){
                while(j < b-1 && matrix[i][j] == matrix[i][j+1]){
                    c++; j++;
                }
                c++;
                if(c > max) {
                    max = c;
                    ans = i;
                }
            }
        }

        return ans;
    }
}

public class Main {
    public static void main(String[] args) {
        System.out.println("Choose your task(1-3): ");
        Scanner in = new Scanner(System.in);
        int a = in.nextInt();
        if(a == 1){
            task1 task = new task1();
            System.out.print("Your answer is: ");
            System.out.println(task.Main());
        }
    }
}