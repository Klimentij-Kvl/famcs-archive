package org.example;

import java.util.*;

public class Main {
    public static void main(String[] args) throws InterruptedException{
        Scanner sc = new Scanner(System.in);
        System.out.println("Type size of your array: ");
        int n = sc.nextInt();

        Arr arr = new Arr();
        arr.arr = new ArrayList<>();
        for(int i = 0; i < n; i++){
            arr.arr.add((int)(Math.random() * 100 % n));
            System.out.print(arr.arr.get(i) + " ");
        }
        System.out.println("\nType up or down: ");
        arr.sortType = sc.next();
        arr.start();
        arr.join();
        for(int i = 0; i < n; i++){
            System.out.print(arr.arr.get(i) + " ");
        }
        sc.close();
    }
}