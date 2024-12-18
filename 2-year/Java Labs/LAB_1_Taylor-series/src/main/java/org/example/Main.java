package org.example;

import java.util.Scanner;

class teyor {
    public static double solve(double x, int k){
        double a=x, b=-1000, e = Math.pow(10, -k), res=x;
        int n = 1;
        while(Math.abs(res-b) > e){
            a = a * Math.pow(x, 2) * (2*n - 1) * (2*(n-1)+1) / (2*n) / (2*n+1);
            b = res;
            res+=a;
            n++;
        }

        return res;
    }
}

public class Main {
    public static void main(String[] args){
        int a;
        double b;
        Scanner in = new Scanner(System.in);


        System.out.print("Write real and int number: ");
        b = in.nextDouble();
        a = in.nextInt();

        teyor Solver = new teyor();

        System.out.println("your answer: " + Math.round(Math.asin(b) * Math.pow(10, a)) / Math.pow(10,a) + " " + Math.round(Solver.solve(b, a*2) * Math.pow(10,a))  / Math.pow(10,a));
        System.out.println(Math.asin(b));
    }
}

/*public class Main2 {
    public static void main(String[] args){
        int a;
        double b;
        Scanner in = new Scanner(System.in);


        System.out.print("Write real and int number: ");
        b = in.nextDouble();
        a = in.nextInt();

        com.company.teyor Solver = new com.company.teyor();

        System.out.println("your answer: " + Math.round(b * Math.pow(10, a)) / Math.pow(10,a));
    }
}*/