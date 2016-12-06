package tiy.networking;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.ArrayList;

/**
 * Created by Corey Shaw on 4/28/2016.
 */

public class ServerThread implements Runnable {

    Socket clientSocket;
    SimpleServer chatServer;
    String emptyString;

    public ServerThread (Socket clientSocket, SimpleServer chatServer){
        this.clientSocket = clientSocket;
        this.chatServer = chatServer;
}

    public void run() {

try{
          // display information about who just connected to our server
        System.out.println("Incoming connection from " + clientSocket.getInetAddress().getHostAddress());

        // this is how we read from the client
        BufferedReader inputFromClient = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));

        // this is how we write back to the client
        PrintWriter outputToClient = new PrintWriter(clientSocket.getOutputStream(), true);
        //give clientSocket a userName
          String userName = clientSocket.toString();
        //Read sockets message
          String inputLine;
          while ((inputLine = inputFromClient.readLine()) != null) {

              System.out.println("Received message: " + inputLine + " from " + clientSocket.toString());
          //    outputToClient.println("Recent message : " + inputLine);

              Message clientMessage = new Message(
                      clientSocket.getInetAddress().getHostAddress(), inputLine);
              chatServer.messageHistory.add(clientMessage);

              for (Message currentMessage : chatServer.messageHistory) {


                outputToClient.println(currentMessage.name + " sent **" +  currentMessage.text +"**   @ " + currentMessage.date);
                 // outputToClient.println( currentMessage.text );

                  //   outputToClient.println("Message added to array");
                  //  Message message = new Message(userName,inputLine);

                  //  storeMessages.addMessage(lastMessage);
                  //       System.out.println(message);
                  //    outputToClient.println(storeMessages.messageArrayList);
              }    outputToClient.println("end-transmission");
          }
    } catch (Exception exception) {
    }



    }
}