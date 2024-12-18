package org.example.lab5;

import javafx.fxml.FXML;
import javafx.scene.control.*;
import javafx.scene.input.MouseEvent;

import java.util.List;

public class HelloController {
    @FXML
    private RadioButton pozd1, pozd2, pozd3, gift1, gift2, gift3, gift4, yes, no;
    @FXML
    private Button button;
    @FXML
    private Label label;
    private ToggleGroup group1, group2, group3;

    @FXML
    void initialize(){
        group1 = new ToggleGroup();
        group2 = new ToggleGroup();
        group3 = new ToggleGroup();

        pozd1.setToggleGroup(group1);
        pozd2.setToggleGroup(group1);
        pozd3.setToggleGroup(group1);

        gift1.setToggleGroup(group2);
        gift2.setToggleGroup(group2);
        gift3.setToggleGroup(group2);
        gift4.setToggleGroup(group2);

        yes.setToggleGroup(group3);
        no.setToggleGroup(group3);
    }

    @FXML
    void buttonClicked(){
        int a,b,c;
        if(pozd1.isSelected()) a = 1000;
        else if(pozd2.isSelected()) a = 1500;
        else if(pozd3.isSelected()) a = 3000;
        else a = 0;

        if(gift1.isSelected()) b = 500;
        else if(gift2.isSelected()) b = 800;
        else if(gift3.isSelected()) b = 50;
        else if(gift4.isSelected()) b= 70;
        else b = 0;

        if(yes.isSelected()) c = 15000;
        else c = 0;

        label.setText(String.valueOf(a+b+c));
    }
}