package org.example.tabledb;

public class Person {
    private int id;
    private String name;
    private int age;

    Person(int id, String name, int age){
        this.id = id;
        this.name = name;
        this.age = age;
    }

    public int getId(){
        return id;
    }

    public String getName(){
        return name;
    }

    public int getAge(){
        return age;
    }

    @Override
    public String toString(){
        return this.name;
    }
}
