package net.chat;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

/**
 * Created by Irina on 23.05.2014.
 */
public class Server {
    private ServerSocket serverSocket;
    private Socket socket;

    public Server() throws IOException {
        serverSocket = new ServerSocket(4321);
        while(true) {
            socket = serverSocket.accept();
            
        }
    }
}
