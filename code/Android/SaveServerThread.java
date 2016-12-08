package tiy.networking;

import java.util.Scanner;

/**
 * Created by Tisha868 on 5/5/16.
 */
public class SaveServerThread implements Runnable { // have to make it runnable interface has 1 method 1= run that cant
// throw exception.

    public  SimpleServer savedThread;

    public SaveServerThread (SimpleServer classThread) {
        savedThread = classThread;
    }
    public void run() { //run method.


        System.out.println("Running " + Thread.currentThread().getId());

        Scanner inputScanner = new Scanner(System.in); // sccnner is int.
        String serverCommand = inputScanner.nextLine();



        if (serverCommand.equals("gold")) { // string called gold
            savedThread.saveServer();
        }


        try {
            Thread.sleep(2000); //Thread.sleep throws exception. All it does is sleep for 2000 miliseconds = 2
            // seconds
        } catch (Exception exception) {
            exception.printStackTrace();
        }

        System.out.println("Done running " + Thread.currentThread().getId());

    }
}
