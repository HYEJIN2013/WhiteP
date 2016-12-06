package tiy.networking;

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;
import java.util.Scanner;

/**
 * Created by Corey Shaw on 4/27/2016.
 */
public class SimpleServer {
    private static final int PORT = 8005;
    private static Scanner lineScanner;
    DataOutputStream dataOutputStream;
    DataInputStream dataInputStream;

    // an array list that holds all the messages
   public  ArrayList<Message> messageHistory = new ArrayList<Message>();

    public static void main(String[] args) throws Exception {
        System.out.println("Running Simple Server!!");
        new SimpleServer().startServer();
    }

       public void startServer()throws Exception {
           ServerSocket serverListener = new ServerSocket(8005);
           while (true) {
            try {
                //Have client accept to connect and run information or display
                Socket clientSocket = serverListener.accept();

                //Start a new thread that takes on new clients.
                ServerThread localThread = new ServerThread(clientSocket,this);
                Thread newThread = new Thread(localThread);
                newThread.start();
            // display information if a client closes a connection.
            } catch (Exception exception) {
                System.out.println("Client closed connection ! (How rude!!! )");
            }
        }
    }
}



//                                                   Extra Information now found in ServerThread Class

/*      System.out.println("Incoming connection from " + clientSocket.getInetAddress().getHostAddress());

                // this is how we read from the client
                BufferedReader inputFromClient = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));

                // this is how we write back to the client
                PrintWriter outputToClient = new PrintWriter(clientSocket.getOutputStream(), true);

                String inputLine;
                while ((inputLine = inputFromClient.readLine()) != null) {
                    System.out.println("Received message: " +
                            inputLine + " from " + clientSocket.toString());
                    outputToClient.println("Message received loud and clear");
                }
            */