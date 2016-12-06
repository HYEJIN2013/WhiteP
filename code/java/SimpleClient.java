package tiy.networking;

import jodd.json.JsonParser;
import jodd.json.JsonSerializer;

import java.io.*;
import java.net.Socket;
import java.util.ArrayList;
import java.util.Scanner;

/**
 * Created by Corey Shaw on 4/27/2016.
 */
public class SimpleClient {


    public static Scanner lineScanner = new Scanner(System.in);
    public static ArrayList<String> messageHistory = new ArrayList<>();
    public static String saveChatMessages = "saveChatMessages.json";


    public static void main(String[] args) throws Exception {
        // Start a local host 8005  every computer is a local host
        // connect to the server on the target port and then connected
        Socket clientSocket = new Socket("172.168.4.10", 8005);
        // once we connect to the server, we also have an input and output stream
        PrintWriter outPut = new PrintWriter(clientSocket.getOutputStream(), true);
        BufferedReader inPut = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
        // send the server an arbitrary message
        Scanner inputScanner = new Scanner(System.in);

        while (true) {
            String message = inputScanner.nextLine();
            outPut.println(message);
            clearScreen();
            if (message.equals("History")) {clearScreen();
                retrieveItemList();
        }
            if (message.equals("exit")) {
                // close the connection
                clientSocket.close();
            } else {
                    String serverMessage = inPut.readLine();
                     messageHistory.clear();
                    while (serverMessage != null) {
                    // String serverResponse =
            //        System.out.println("( Message from Server : " + serverMessage + " )");
                        System.out.println( serverMessage );
                    messageHistory.add(serverMessage);
                        messageHistory.spliterator();
                    serverMessage = inPut.readLine();


                    if (serverMessage.equals("end-transmission")) {//   System.out.println("Message history added to array---> " + messageHistory);
                        saveItem();  clearScreen();
                        break;
                    }

                }


            }

        }

 }


    public static void saveItem() {

        try {
            File jsonFile = new File(saveChatMessages);


        //    System.out.println("Saving  item ...");
            JsonSerializer jsonSerializer = new JsonSerializer().deep(true);

            String jsonString = jsonSerializer.serialize(messageHistory);


            FileWriter jsonWriter = new FileWriter(saveChatMessages);

            jsonWriter.write(jsonString);
            jsonWriter.close();


        } catch (IOException exception) {
        }


    }

    public static void retrieveItemList() {

        // ArrayList<ToDoItem> myArray = new ArrayList<>(todoItems);

        try {

            Scanner fileScanner = new Scanner(new File(saveChatMessages));
            fileScanner.useDelimiter("\\Z");
            String fileContents = fileScanner.next();
            JsonParser messageParser = new JsonParser();
            messageHistory = messageParser.parse(fileContents);
            System.out.println("=================================");
            System.out.println("    Beginning of  Message History                     ");

            for(int count = 0; count < messageHistory.size(); count ++) {
                System.out.println(messageHistory.get(count));
            }
            System.out.println("       Ending of Message History            ");
            System.out.println("====================================");


            // for(int counter =0; counter < return ToDoItem.todoItems.size(); counter++ ){


            //  }

            //return returnToDoItems;

        } catch (IOException ioException) {

            //  return null;
        }

    }


    public static void clearScreen() throws Exception{
        new ProcessBuilder("cmd", "/c", "cls").inheritIO().start().waitFor();
    }




}