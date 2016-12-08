package net.chat;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;

/**
 * Created by Irina on 23.05.2014.
 */
public class ClientHandler implements Runnable {
    private Socket incoming;
    private InputStream inStream;
    private OutputStream outStream;
    
    public ClientHandler(Socket incoming) throws IOException {
        this.incoming = incoming;
        this.inStream = incoming.getInputStream();
        this.outStream = incoming.getOutputStream();
    }
    @Override
    public void run() {
        
    }
}
