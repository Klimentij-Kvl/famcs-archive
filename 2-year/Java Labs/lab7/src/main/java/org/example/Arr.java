package org.example;

import java.util.Comparator;
import java.util.List;

public class Arr extends Thread{
    public List<Integer> arr;
    public String sortType;

    public void run(){
        Comparator<Integer> comp;
        if(sortType.equals("up"))
            comp = Comparator.naturalOrder();
        else
            comp = Comparator.reverseOrder();

        arr.sort(comp);
    }
}