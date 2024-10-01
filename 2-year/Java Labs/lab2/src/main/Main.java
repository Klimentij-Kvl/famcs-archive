package main;

import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        int a, b;
        Scanner in = new Scanner(System.in);
        System.out.println("Type a and b - size of your matrix: ");
        a = in.nextInt(); b = in.nextInt();

        int[][] matrix = new int[a][b];
        System.out.println("Type your matrix: ");
        for(int i = 0; i < a; i++) {
            for (int j = 0; j < b; j++) {
                matrix[i][j] = in.nextInt();
            }
        }

        System.out.println("Choose your task(1-3): ");
        int task = in.nextInt();
        if(task == 1){
            task1 Task = new task1();
            System.out.printf("Your answer is: %d", Task.Main(a,b,matrix));
        }
        if(task == 2){
            task2 Task = new task2();
            System.out.printf("Your answer is: %d", Task.Main(a,b,matrix));
        }
    }
}