module org.example.tabledb {
    requires javafx.controls;
    requires javafx.fxml;
    requires java.sql;


    opens org.example.tabledb to javafx.fxml;
    exports org.example.tabledb;
}