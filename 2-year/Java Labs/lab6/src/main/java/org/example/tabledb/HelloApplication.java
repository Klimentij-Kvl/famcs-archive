package org.example.tabledb;

import javafx.application.Application;
import javafx.beans.Observable;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.scene.layout.FlowPane;
import javafx.stage.Stage;

import java.io.IOException;
import java.sql.*;

public class HelloApplication extends Application {
    @Override
    public void start(Stage stage) throws IOException, SQLException{
        Connection connection = DriverManager.getConnection("jdbc:mysql://localhost/users", "root", "1989");
        ObservableList<Person> people = FXCollections.observableArrayList();
        Statement statement = connection.createStatement();
        ResultSet resultSet = statement.executeQuery("SELECT * FROM people");
        while(resultSet.next()){
            people.add(new Person(resultSet.getInt(1), resultSet.getString(2),
                    resultSet.getInt(3)));
        }
        connection.close();

        TableView<Person> table = new TableView<Person>(people);
        table.setPrefWidth(250);
        table.setPrefHeight(200);

        TableColumn<Person, Integer> idColumn = new TableColumn<>("id");
        idColumn.setCellValueFactory(new PropertyValueFactory<Person, Integer>("id"));
        table.getColumns().add(idColumn);

        TableColumn<Person, String> nameColumn = new TableColumn<>("name");
        nameColumn.setCellValueFactory(new PropertyValueFactory<Person, String>("name"));
        table.getColumns().add(nameColumn);

        TableColumn<Person, Integer> ageColumn = new TableColumn<>("age");
        ageColumn.setCellValueFactory(new PropertyValueFactory<Person, Integer>("age"));
        table.getColumns().add(ageColumn);

        //FXMLLoader fxmlLoader = new FXMLLoader(HelloApplication.class.getResource("hello-view.fxml"));
        FlowPane root = new FlowPane(10,10,table);
        Scene scene = new Scene(root, 320, 240);
        stage.setTitle("Database");
        stage.setScene(scene);
        stage.show();
    }

    public static void main(String[] args) {
        launch();
        //java -classpath c:\Java\mysql-connector-java-8.0.11.jar;c:\Java Program

    }
}