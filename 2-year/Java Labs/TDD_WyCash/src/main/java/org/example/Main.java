package org.example;

import java.util.Hashtable;

interface Expression{
    Money reduce(Bank bank, String to);
    Expression plus(Expression addend);
    Expression times(int multiplier);
}

class Sum  implements Expression{
    Expression augend;
    Expression addend;
    Sum(Expression augend, Expression addend){
        this.augend = augend;
        this.addend = addend;
    }

    public Expression times(int multiplier){
        return new Sum(augend.times(multiplier), addend.times(multiplier));
    }

    public Money reduce(Bank bank, String to){
        int amount = augend.reduce(bank, to).amount + addend.reduce(bank, to).amount;
        return new Money(amount, to);
    }

    public Expression plus(Expression addend){
        return new Sum(this, addend);
    }
}

class Bank{
    private class Pair{
        private String from;
        private String to;

        Pair(String from, String to){
            this.from = from;
            this.to = to;
        }

        public boolean equals(Object object){
            Pair pair = (Pair)object;
            return from.equals(pair.from) && to.equals(pair.to);
        }

        public int hashCode(){
            return 0;
        }
    }

    private Hashtable rates = new Hashtable();

    void addRate(String  from, String to, int rate){
        rates.put(new Pair(from, to), Integer.valueOf(rate));
    }

    int rate(String from, String to){
        if(from.equals(to)) return 1;
        Integer rate = (Integer)rates.get(new Pair(from, to));
        return rate.intValue();
    }

    Money reduce(Expression source, String to){
        return source.reduce(this, to);
    }
}

class Money implements Expression{
    protected int amount;
    protected String currency;

    Money(int amount, String currency){
        this.amount = amount;
        this.currency = currency;
    }

    public Money reduce(Bank bank, String to){
        int rate = bank.rate(currency, to);
        return new Money(amount / rate, to);
    }

    public Expression times(int multiplier){
        return new Money(amount*multiplier, currency);
    };

    String currency(){
        return currency;
    }

    static Money dollar(int amount){
        return new Money(amount, "USD");
    }

    static Money franc(int amount){
        return new Money(amount, "CHF");
    }

    public boolean equals(Object object){
        Money money = (Money)object;
        return amount == money.amount && currency().equals(money.currency());
    }

    public Expression plus(Expression addend){
        return new Sum(this, addend);
    }

    public String toString(){
        return amount + " " + currency;
    }
}



public class Main {
    public static void main(String[] args) {
        System.out.println("Hello world!");
    }
}