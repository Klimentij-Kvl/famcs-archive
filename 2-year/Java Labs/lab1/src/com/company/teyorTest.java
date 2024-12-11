package com.company;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class teyorTest {

    @Test
    void solve1() {
        double x = teyor.solve(0.5, 4);
        assertEquals(0.52359, x, 0.00001);
    }

    @Test
    void solve2(){
        double x = teyor.solve(0.3, 10);
        assertEquals(0.304692654, x, 0.000000001);
    }

    @Test
    void solve3(){
        double x = teyor.solve(0.99, 16);
        assertEquals(1.42925685, x, 0.00000001);
    }
}