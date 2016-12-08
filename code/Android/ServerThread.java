package tiy.networking;

import tiy.networking.SimpleServer;

import java.io.*;
import java.net.Socket;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;



public class ServerThread implements Runnable{

    public static String clientName; // declaring a variable instant of data type string
    public static String inputLine;
    public static String clientTimeStamp;
    public SimpleServer classMessage;
    public Socket clientSocket; // delcaring clientSocket in this class

    //public MessageLog messageLogs = new MessageLog(); // contains the array list

   // this.chatServer = chatServer
   public String saveHistory; // just a variable


    public ServerThread(Socket userSocket, SimpleServer incomingMessage) { // making a constructor of the Thread. Every
        // object needs a constructor.
        clientSocket = userSocket;
        classMessage = incomingMessage;
    }

    public void run() {

        System.out.println("~~*~~ Running ^.^ The Chat Room ~~*~~");

        try {
            // Socket clientSocket = serverListener.accept(); // accept connection

            // display information about who just connected to our server
            System.out.println("Incoming connection from: " + clientSocket.getInetAddress().getHostAddress());

            // this is how we read from the client
            BufferedReader inputFromClient = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
            // this is how we write back to the client
            PrintWriter outputToClient = new PrintWriter(clientSocket.getOutputStream(), true);

            clientName = clientSocket.getInetAddress().getHostAddress(); // stored a value of the Clients


            // IP Address in2 a variable.
            // read from input screen until theres nothing left to read, input screen is what the client is telling us.
            // read from the input until the client disconnects
            // String inputLine; // declaring of data type of string called inputLine
            while ((inputLine = inputFromClient.readLine()) != null) { // call a method of inputFromClient is
                // going to readLIne and storing it into inputLine. != boolean statment

                LocalDateTime now = LocalDateTime.now();
                DateTimeFormatter LocalDateTime = DateTimeFormatter.ofPattern("MMM d,yyyy @ hh:mm a");
                clientTimeStamp = now.format(LocalDateTime).toString();



                Message clientMessage = new Message(inputLine, clientName, clientTimeStamp);  // cre8ing an
                // instance of an object
                classMessage.messageThings.add(clientMessage); // Saved all the messages that each client sends
                // into a data structure. stored all this info classMessage into an array list.

                ArrayList<Message> messageThings = classMessage.messageThings;
                // when you're calling an item more than 1nce,
                for (int counter = 0; counter < messageThings.size(); counter++) {
                    outputToClient.println(messageThings.get(counter).toString());
                    System.out.println("Message ~To~ Server -->> " + messageThings.get(counter).toString()); // + " from:
                    // " +
                    // clientSocket.toString());

                    //outputToClient.println("Message received: " + inputLine); // sending it to the client
                }
                System.out.println("~~*~~~~*~~~~*~~~~*~~~~*~~~~*~~~~*~~~~*~~~~*~~~~*~~");
                outputToClient.println("end-transmission");

            }

        }catch(IOException exception){
            System.out.println("Client has Exited Chat Room :/ ");
        }
    }

}

