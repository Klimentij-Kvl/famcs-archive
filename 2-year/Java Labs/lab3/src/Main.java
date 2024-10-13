import java.io.File;
import java.io.IOException;
import java.util.*;
import java.util.stream.Stream;

class gradeBook {

    class Session{
        class Subject{
            private String name;
            private int mark;

            Subject(String subjName, int subjMark){
                name = subjName;
                mark = subjMark;
            }

            int getMark(){
                return mark;
            }

            void show(){
                System.out.print(name + " " + mark + " ");
            }
        }

        Vector<Subject> subjects;

        Session(){
            subjects = new Vector<>();
        }

        void addSubject(String subjName, int mark){
            subjects.add(new Subject(subjName, mark));
        }

        void show(){
            for(Subject j : subjects)
                j.show();
        }
    }

    private String name;
    private String secondName;
    private String surname;
    private int year;
    private int group;
    private HashMap<Integer, Session> sessions;


    gradeBook(String studentSecondName, String studentName, String studentSurname, int studentYear, int studentGroup){
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
            sessions.put(sessionNum, new Session());
        }
    }

    void show(){
        System.out.println(secondName +" " + name + " " + surname + " "
                + year + " " + group);
    }}

public class Main {
    public static void main(String[] args) {
        HashMap<Integer, gradeBook> students = new HashMap<>();
        File studFile = new File("students.txt");
        try {
            Scanner in = new Scanner(studFile);
            int i = 1;
            Date current = new Date();
            while(in.hasNext()){
                students.put(current.getYear() * 1000 + i, new gradeBook(in.next(), in.next(),
                        in.next(), in.nextInt(), in.nextInt()));
                i++;
            }
            for(Integer j : new TreeSet<>(students.keySet())){
                System.out.print(j + " ");
                students.get(j).show();
            }

            Scanner cin = new Scanner(System.in);
            String s, subject;
            int session, course, group, stud;
            File subj;
            while(true){
                s = cin.next();
                if(s.equals("0")){
                    break;
                }
                subj = new File(s);
                in = new Scanner(subj);
                subject = in.next();
                session = in.nextInt(); course = in.nextInt(); group = in.nextInt();
                while(in.hasNext()){
                    students.get(in.nextInt()) = 
                }
            }
        }catch(IOException e){
            System.out.println(e.getMessage());
        }
    }
}