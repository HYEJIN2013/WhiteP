package com.javarush.test.level30.lesson15.big01;

import java.io.*;
import java.net.Socket;
import java.net.SocketAddress;

/**
 * Created by user-pc on 20.05.2016.
 */
public class Connection implements Serializable, Closeable {
    private final Socket socket;
    private final ObjectOutputStream out;
    private final ObjectInputStream in;

    public Connection(Socket socket) throws IOException {
        this.socket = socket;
        out = new ObjectOutputStream(socket.getOutputStream());
        in = new ObjectInputStream(socket.getInputStream());
    }

    public void send(Message message) throws IOException {
        synchronized (out) {
            out.writeObject(message);
            out.flush();
        }
    }
    public Message receive() throws IOException, ClassNotFoundException {
        synchronized (in) {
            return (Message) in.readObject();
        }
    }
    public SocketAddress getRemoteSocketAddress() {
        return socket.getRemoteSocketAddress();
    }

    public void close() throws IOException {
        socket.close();
        out.close();
        in.close();
    }
}
