import java.io.File;
import java.io.IOException;
import java.util.Scanner;
import java.util.ArrayList;

class diploma {
    public String name;
    public String champ;
    public int num;

    diploma(){
    }

    diploma(diploma dip){
        name = dip.name;
        champ = dip.champ;
        num = dip.num;
    }
}

public class creationList {
    private final ArrayList<diploma> diplomas;

    creationList(){
        diplomas = new ArrayList<>();
    }

    public void readFile(String fileName){
        File ifile;
        ifile = new File(fileName);
        try {
            Scanner in = new Scanner(ifile);
            //in.useDelimiter(" ");
            diploma dip = new diploma();
            while(in.hasNext()){
                dip.name = in.next();
                dip.champ = in.next();
                dip.num = in.nextInt();
                diplomas.add(new diploma(dip));
            }
            in.close();
        }catch(IOException ex) {
            System.out.println(ex.getMessage());
        }
    }

    public void writeFileToConsole(){
        for(diploma dip : diplomas){
            System.out.println(dip.name + " " + dip.champ + " " + dip.num);
        }
    }
}