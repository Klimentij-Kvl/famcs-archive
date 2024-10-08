package main;

import java.io.IOException;
import java.io.File;
import java.io.PrintStream;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
    try {
        File inFile = new File("input.txt");
        Scanner in = new Scanner(inFile);
        PrintStream out = new PrintStream("output.txt");

        int task = in.nextInt();

        if (task == 4) {
            int a;
            a = in.nextInt();

            int[][] matrix = new int[a][a];

            for (int i = 0; i < a; i++) {
                for (int j = 0; j < a; j++) {
                    matrix[i][j] = in.nextInt();
                }
            }

            task4 Task = new task4();
            out.printf("Your answer: %f", Task.Main(a, matrix));

            return;
        }

        int a, b;
        a = in.nextInt();
        b = in.nextInt();

        int[][] matrix = new int[a][b];
        for (int i = 0; i < a; i++) {
            for (int j = 0; j < b; j++) {
                matrix[i][j] = in.nextInt();
            }
        }


        if (task == 1) {
            task1 Task = new task1();
            out.printf("Your answer is: %d", Task.Main(a, b, matrix));
        }
        if (task == 2) {
            task2 Task = new task2();
            out.printf("Your answer is: %d", Task.Main(a, b, matrix));
        }
        if (task == 3) {
            task3 Task = new task3();
            int[][] ans = Task.Main(a, b, matrix);
            for (int i = 0; i < a; i++) {
                for (int j = 0; j < b; j++) {
                    out.printf("%d ", ans[i][j]);
                }
                out.println();
            }
        }
    }catch(IOException e){
        System.out.println(e.getMessage());
    }
    }
}