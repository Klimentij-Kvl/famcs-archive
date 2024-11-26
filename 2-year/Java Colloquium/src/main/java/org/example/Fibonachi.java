package org.example;

import java.util.ArrayList;
import java.util.List;

public class Fibonachi{

    public static List<Long> makeFibonachiList(int n){
        if(n > 93){
            System.out.println("Too big number for function");
            return null;
        }
        if(n < 1){
            System.out.println("Too little number for function");
            return null;
        }
        List<Long> arr = new ArrayList<>();
        long a = 0, b = 1, c;
        for(int i = 0; i < n; i++){
            arr.add(a);
            b+=a;
            a = b-a;
        }

        return arr;
    }
}
