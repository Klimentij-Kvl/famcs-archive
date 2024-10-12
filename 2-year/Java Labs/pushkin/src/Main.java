import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;

public class Main {
    public static void main(String[] args) {

        try{
            FileWriter out = new FileWriter("output.txt");
            StringTokenizer str =
                    new StringTokenizer(Files.readString(Path.of("input.txt")).toLowerCase(),
                            " \n\t\r,.:;()");
            LinkedHashSet<String> set = new LinkedHashSet<>();
            while(str.hasMoreTokens()){
                set.add(str.nextToken());
            }
            for(String s: set){
                out.write(s + " ");
            }
            out.write("\n\n\n"+ "Number of words: " + set.size());
            out.close();
        }catch(IOException e){
            System.out.println(e.getMessage());
        }
    }
}