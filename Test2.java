import java.util.Scanner;

public class Test2{

    public static void main(String[] args){
                Scanner scnr = new Scanner(System.in);
                System.out.println("Enter a letter");
                String inputLetter = scnr.next();
                char myLetter = inputLetter.charAt(0);

                switch(myLetter){

                	case 'A':
                	case 'B':
                	case 'C':
                		System.out.println("You entered an A, B or C");
                		break;
                	case 'D':
                		System.out.println("You entered a D");
                		break;	
                	default:
                		System.out.println("You entered something besides A,B,C,D");
                		break;
                
                }
                
                boolean isRed = false;
                boolean isApple = true;

                if (isRed && isApple){
                	System.out.println("IT IS AN APPLE");
                }
                else if (isRed){
                	System.out.println("JUST SOMETHING THAT IS RED");
                }
                else{
                	System.out.println("WHO KNOWS?");
                }
                

        }        

}