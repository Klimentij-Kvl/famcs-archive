package org.example.tabledb;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class DBConnection {
    private static DBConnection instance = null;
    public static DBConnection getInstance() throws SQLException{
        if(instance == null)
            instance = new DBConnection();

        return instance;
    }

    public Connection getConnection(){
        Connection connection = null;
        try{
            connection = DriverManager.getConnection("jdbc:mysql://localhost/Users","root","1989");
        }
        catch(SQLException e){
            System.out.println(e.getErrorCode());
        }

        return connection;
    }
}
