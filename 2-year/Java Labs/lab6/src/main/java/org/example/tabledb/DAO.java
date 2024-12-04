package org.example.tabledb;

import javafx.collections.ObservableList;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

public class DAO {
    private static final DAO INSTANCE = new DAO();
    public static DAO getInstance(){
        return INSTANCE;
    }

    public List<Person> findAll(){
        try(Connection connection = DBConnection.getInstance().getConnection()){
            Statement statement = connection.createStatement();
            ResultSet resultSet = statement.executeQuery("SELECT * FROM people");
            List<Person> ans = new ArrayList<>();
            while(resultSet.next()){
                ans.add(buildPerson(resultSet));
            }
            return ans;
        }catch (SQLException e){
            System.out.println(e.getErrorCode());
            return null;
        }
    }

    public void saveAll(ObservableList<Person> people){
        try(Connection connection = DBConnection.getInstance().getConnection()){
            Statement statement = connection.createStatement();
            int id = 1;
            for(Person p : people){
                statement.execute("update people set Name = '" + p.getName() + "', Age = " + p.getAge() + " where Id = " + id);
                id++;
            }
        }catch (SQLException e){
            System.out.println(e.getErrorCode());
        }
    }

    private Person buildPerson(ResultSet resultSet) throws SQLException{
        return new Person(resultSet.getInt(1), resultSet.getString(2), resultSet.getInt(3));
    }
}
