package com.example.demo1;

import javafx.fxml.FXML;
import javafx.scene.control.CheckBox;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;

public class HelloController {
    @FXML private Label welcomeText;
     @FXML private Label answerLabel;
    @FXML private TextField field1;
    @FXML private TextField field2;
    @FXML private CheckBox org1;
    @FXML private CheckBox org2;
    @FXML private CheckBox org3;

    @FXML private CheckBox prize1;
    @FXML private CheckBox prize2;
    @FXML private CheckBox prize3;
    @FXML private CheckBox prize4;

    @FXML private CheckBox concYes;
    @FXML private CheckBox concNo;
    @FXML private CheckBox clientYes;
    @FXML private CheckBox clientNo;

    private int n;

    @FXML
    public void initialize() {
        System.out.println("roflokek");
    }

    @FXML
    protected void onHelloButtonClick() {
        answerLabel.setText(String.valueOf(Integer.valueOf(field1.getText()) + Integer.valueOf(field2.getText())));
    }
    @FXML
    private void show1(){
        if(org1.isSelected()){
            org2.setSelected(false);
            org3.setSelected(false);
        }
        else if(org2.isSelected()){
            org1.setSelected(false);
            org3.setSelected(false);
        }
        else if(org3.isSelected()){
            org1.setSelected(false);
            org2.setSelected(false);
        }
    }
    @FXML
    private void show2(){}

}