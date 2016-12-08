package tiy.networking;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.Scanner;

/**
 * Created by Tisha868 on 4/27/16.
 */
public class SimpleClient {

    public static void main(String[] args) throws Exception {


        //intalize client screen
        // connect to the server on the target port
       // String client1 = "172.168.4.9"; // <-- stores IP Address into persons name, WIthOUT "" marks
        Socket clientSocket = new Socket("localhost",8005);
        // "localhost" = connects to self
        // changed the clientSocket to connect to the server computer's IP address instead of "localhost".
        // i want to connect on my local host on port 8005

        while (true) { // for (int count = 0; count < 3; count++) {} = sent 3 messages in a loop.
            System.out.println("Enter message below");
            System.out.print(">");
            Scanner clientScanner = new Scanner(System.in); // <-- is the input
            String currentLine = clientScanner.nextLine();
            // the connection
            PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true);
            BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));

            // send the server a message
            out.println(currentLine);
            String serverResponse;

            while (true) { // will print out evetyhing the sevrer is  sending back.
                // read what the server returns
                serverResponse = in.readLine(); // input 4rm server

                if (serverResponse.equals("end-transmission")){
                    break;
                }

                System.out.println(serverResponse);
            }
//            if (currentLine.equals("exit")) {
//                // close the connection
//                clientSocket.close();
//                break;
//            }
        }
    }

}