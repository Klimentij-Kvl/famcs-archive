package main;

import java.util.Scanner;

public class Main {
    public static void main(String[] args) {

        Scanner in = new Scanner(System.in);
        System.out.println("Choose your task(1-4): ");
        int task = in.nextInt();

        if(task == 4){
            int a;
            System.out.println("Type a - size of your matrix: ");
            a = in.nextInt();

            int[][] matrix = new int[a][a];

            System.out.println("Type your matrix: ");
            for(int i = 0; i < a; i++) {
                for (int j = 0; j < a; j++) {
                    matrix[i][j] = in.nextInt();
                }
            }

            task4 Task = new task4();
            System.out.printf("Your answer: %f", Task.Main(a,matrix));

            return;
        }

        int a, b;
        System.out.println("Type a and b - size of your matrix: ");
        a = in.nextInt(); b = in.nextInt();

        int[][] matrix = new int[a][b];
        System.out.println("Type your matrix: ");
        for(int i = 0; i < a; i++) {
            for (int j = 0; j < b; j++) {
                matrix[i][j] = in.nextInt();
            }
        }


        if(task == 1){
            task1 Task = new task1();
            System.out.printf("Your answer is: %d", Task.Main(a,b,matrix));
        }
        if(task == 2){
            task2 Task = new task2();
            System.out.printf("Your answer is: %d", Task.Main(a,b,matrix));
        }
        if(task == 3){
            task3 Task = new task3();
            int[][] ans = Task.Main(a,b,matrix);
            System.out.println("Your answer: ");
            for(int i = 0; i < a; i++){
                for(int j = 0; j < b; j++){
                    System.out.printf("%d ", ans[i][j]);
                }
                System.out.println();
            }
        }

    }
}