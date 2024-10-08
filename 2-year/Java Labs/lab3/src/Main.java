import java.io.File;
import java.io.IOException;
import java.util.Date;
import java.util.HashMap;
import java.util.Scanner;

class gradeBook {

    class Session{
        HashMap<String, Integer> subjectsAndMarks;

        Session(){
            subjectsAndMarks= new HashMap<>();
        }

        Session(String subjName, int mark){
            subjectsAndMarks= new HashMap<>();
            subjectsAndMarks.put(subjName, mark);
        }

        void addSubject(String subjName, int mark){
            subjectsAndMarks.put(subjName, mark);
        }
    }

    private String name;
    private String secondName;
    private String surname;
    private int year;
    private int group;
    private HashMap<Integer, Session> sessions;


    gradeBook(String studentName, String studentSecondName, String studentSurname, int studentYear, int studentGroup){
        name = studentName;
        secondName = studentSecondName;
        surname = studentSurname;
        year = studentYear;
        group = studentGroup;
        sessions = new HashMap<>();
    }

    void setPassportData(String studentName, String studentSecondName, String studentSurname) {
        name = studentName;
        secondName = studentSecondName;
        surname = studentSurname;
    }

    void setYear(int studentYear) {
        year = studentYear;
    }

    void setGroup(int studentGroup) {
        group = studentGroup;
    }

    void addSubjectMark(int sessionNum, String subjectName, int mark){
        if(sessions.containsKey(sessionNum)){
            sessions.get(sessionNum).addSubject(subjectName, mark);
        }else{
            sessions.put(sessionNum, new Session(subjectName, mark));
        }
    }
}

public class Main {
    public static void main(String[] args) {
        HashMap<Integer, gradeBook> students = new HashMap<>();
        File studFile = new File("students.txt");
        try {
            Scanner in = new Scanner(studFile);
            int i = 0;
            Date current = new Date();
            while(in.hasNext()){
                students.put(current.getYear() * 1000 + i, new gradeBook(in.next(), in.next(),
                        in.next(), in.nextInt(), in.nextInt()));
            }
        }catch(IOException e){
            System.out.println(e.getMessage());
        }
    }
}