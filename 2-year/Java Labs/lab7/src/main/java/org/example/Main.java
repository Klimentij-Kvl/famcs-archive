package org.example;

import java.util.*;
import java.util.stream.Collectors;

class upIntComp implements Comparator<Integer>{
    public int compare(Integer a, Integer b){
        return a.compareTo(b);
    }
}

class downIntComp implements Comparator<Integer>{
    public int compare(Integer a, Integer b){
        return b.compareTo(a);
    }
}

class Arr extends Thread{
    public List<Integer> arr;
    public String sortType;

    public void run(){
        Comparator<Integer> comp;
        if(sortType.equals("up"))
            comp = Comparator.naturalOrder();
        else
            comp = Comparator.reverseOrder();

        arr.sort(comp);
        //for(int i : arr){
        //    System.out.print(i + " ");
        //}
    }
}

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