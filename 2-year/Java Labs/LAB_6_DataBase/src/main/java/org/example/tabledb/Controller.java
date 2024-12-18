package org.example.tabledb;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.cell.PropertyValueFactory;

import java.net.URL;
import java.sql.*;
import java.util.List;
import java.util.ResourceBundle;

public class Controller{
    private static ObservableList<Person> peopleData = FXCollections.observableArrayList();;

    @FXML
    private TableColumn<Person, Integer> idColumn, ageColumn;
    @FXML
    private TableColumn<Person, String> nameColumn;
    @FXML
    private TableView<Person> table;

    @FXML
    protected void onLoadButtonClick() {
        List<Person> people = DAO.getInstance().findAll();
        for (Person p : people) {
            peopleData.add(new Person(p.getId(), p.getName(), p.getAge()));
        }

        idColumn.setCellValueFactory(new PropertyValueFactory<Person, Integer>("Id"));
        nameColumn.setCellValueFactory(new PropertyValueFactory<Person, String>("Name"));
        ageColumn.setCellValueFactory(new PropertyValueFactory<Person, Integer>("Age"));

        table.setItems(peopleData);
    }

    @FXML
    protected void onSaveButtonClick(){
        peopleData = table.getItems();
        DAO.getInstance().saveAll(peopleData);
    }
}