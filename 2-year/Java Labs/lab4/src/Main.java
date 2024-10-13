import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;
import java.util.StringTokenizer;
import java.nio.file.Files;
import java.nio.file.Path;

class Task{
    void main(String text, int n){
        StringTokenizer str = new StringTokenizer(text, " \n\t\r.,():;", true);
        String s,  vowels="цкнгшщзхфвпрлджчсмтб";
        try {
            FileWriter out = new FileWriter("output.txt");

            while (str.hasMoreTokens()) {
                s = str.nextToken();
                //System.out.println(vowels.indexOf(s.toLowerCase().charAt(0)));
                if (!(s.length() == n && vowels.indexOf(s.toLowerCase().charAt(0)) != -1)) {
                    out.write(s);
                }
            }
            out.close();
        }catch (IOException e){
            System.out.println(e.getMessage());
        }
    }
}

public class Main {
    public static void main(String[] args) {
        Task task = new Task();
        System.out.print("Type a word length: ");
        Scanner in = new Scanner(System.in);
        try{
            task.main(Files.readString(Path.of("input.txt")), in.nextInt());
        }catch(IOException e){
            System.out.println(e.getMessage());
        }
    }
}