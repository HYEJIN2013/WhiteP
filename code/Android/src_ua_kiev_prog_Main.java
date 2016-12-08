package ua.kiev.prog;

import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Scanner;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import javax.swing.*;


class GetThread extends Thread {
    private int n;
    private String login;
    private String room = "";

    public GetThread(String login) {
        this.login = login;
    }

    public GetThread() {
    }

    @Override
    public void run() {
        try {
            while (!isInterrupted()) {
                URL url = new URL("http://localhost:8080/get?from=" + n + "&login=" + login + ((!room.isEmpty()) ? "&room=" + room : ""));
                HttpURLConnection http = (HttpURLConnection) url.openConnection();

                InputStream is = http.getInputStream();
                try {
                    int sz = is.available();
                    if (sz > 0) {
                        byte[] buf = new byte[is.available()];
                        is.read(buf);

                        Gson gson = new GsonBuilder().create();
                        Message[] list = gson.fromJson(new String(buf), Message[].class);

                        for (Message m : list) {
                            System.out.println(m);
                            n++;
                        }
                    }
                } finally {
                    is.close();
                }
            }
        } catch (Exception ex) {
            ex.printStackTrace();
            return;
        }
    }

    public String getRoom() {
        return room;
    }

    public void setRoom(String room) {
        this.room = room;
    }
}

public class Main {

    public static void main(String[] args) {

        Scanner scanner = new Scanner(System.in);
        try {
            System.out.println("Enter login: ");
            String login = scanner.nextLine();

            System.out.println("Enter password: ");
            String pass = scanner.nextLine();

            Message m = new Message();

            m.setFrom(login);
            m.setTo(pass);
            try {
                int res = m.send("http://localhost:8080/login");
                if (res != 200) {
                    System.out.println("Login Error");
                    return;
                }


            } catch (IOException e) {
                e.printStackTrace();

            }


            System.out.println("User " + login);
            GetThread th = new GetThread(login);
            th.setDaemon(true);
            th.start();
            String room = "";
            String buf;
            String url;


            while (true) {
                url = "http://localhost:8080/add";
                String text = scanner.nextLine();
                if (text.isEmpty())
                    break;


                if (text.charAt(0) == '@') {
                    buf = (text.indexOf(" ") == -1) ? text.substring(1, text.length()) : text.substring(1, text.indexOf(": "));
//                    System.out.println(buf);
                    switch (buf) {
                        case "list":
                            url = "http://localhost:8080/list";
                            break;

                        case "status_active":
                            m.setTo("active");
                            url = "http://localhost:8080/status";
                            break;


                        case "status_away":
                            m.setTo("away");
                            url = "http://localhost:8080/status";
                            break;

                        case "connect_room":
                            System.out.println(login + " connect to room");
                            room = "room";
                            th.setRoom("room");

                            continue;
                        case "disconnect_room":
                            System.out.println(login + " disconnect to room");
                            room = "";
                            th.setRoom("");
                            continue;
                        default:
                            m.setTo(buf);
                            m.setText(text);
                    }
                } else {
                    m.setTo("all");
                    m.setText(text);
                }

                m.setRoom(room);

                try {
                    int res = m.send(url);
                    if (res != 200) {
                        System.out.println("HTTP error: " + res);
                        return;
                    }
                } catch (IOException ex) {
                    System.out.println("Error: " + ex.getMessage());
                    return;
                }
            }
        } finally {
            scanner.close();
        }
    }


}
