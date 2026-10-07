package org.example;

class Singleton {
    private int value;
    static Singleton _inst;
    protected Singleton(int value){
        this.value = value;
    }

    public static Singleton getInstance(int value){
        if(_inst == null){
            _inst = new Singleton(value);
        }
        return _inst;
    }

    void setValue(int value){
        this.value = value;
    }

    int getValue(){
        return value;
    }
}

public class Main {
    public static void main(String[] args) {
        Singleton singleton = Singleton.getInstance(5);
        Singleton anotherSingleton = Singleton.getInstance(8);
        System.out.println(singleton.getValue());
        System.out.println(anotherSingleton.getValue());

        singleton.setValue(7);

        System.out.println(singleton.getValue());
        System.out.println(anotherSingleton.getValue());
    }
}