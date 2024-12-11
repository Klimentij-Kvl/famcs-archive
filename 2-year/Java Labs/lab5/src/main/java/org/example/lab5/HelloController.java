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
    void click(){
        int a,b,c;
        if(pozd1.)
    }
}