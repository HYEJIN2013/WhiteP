import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Scanner;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import static java.lang.Thread.sleep;

class GetThread implements Runnable {
    private int n;
    private User user;

    GetThread(User user) {
        this.user = user;
    }

    @Override
    public void run() {

        try {
            while (!Thread.currentThread().isInterrupted()) {

                URL url = new URL("http://localhost:8080/get?from=" + n);
                HttpURLConnection http = (HttpURLConnection) url.openConnection();
                http.setRequestProperty("id", user.getUserId());
                InputStream is = http.getInputStream();

                try {
                    int sz = is.available();
                    if (sz > 0) {


                        Gson gson = new GsonBuilder().create();
                        Message[] list = gson.fromJson(new BufferedReader(new InputStreamReader(is)), Message[].class);

                        for (Message m : list) {
                            if (user.isChatRoomMode()) {if(m.getTo().contains(user.getRoomName())){System.out.println(m);}

                            } else if (m.getTo().contains(user.getLogin()) ||
                                    m.getTo().contains("all") || m.getTo().isEmpty() ||
                                    m.getFrom().equals(user.getLogin())) {//on clients side -its not wery good imho...
                                System.out.println(m);
                            }
                            n++;
                        }
                    }

                } finally {
                    is.close();
                }
                sleep(300);
            }
        } catch (Exception ex) {
            ex.printStackTrace();
            return;
        }
    }
}

public class
Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        try {
            System.out.println("Hello, this is simple chat client. If you need help, enter  ~help.  Enjoy!");
            System.out.println("Enter login: ");
            String login = scanner.nextLine();
            System.out.println("Enter password: ");
            String password = scanner.nextLine();
            User user = new User(login, password);
            try {

                user.logIn(login, password, "http://localhost:8080/login");
                if (!user.getUserId().contains("Denied")) {
                    System.out.println("HTTP authorization: OK ");
                }

            } catch (IOException ex) {
                System.out.println("Error: " + ex.getMessage());
                return;
            }
            GetThread getThread = new GetThread(user);
            Thread th = new Thread(getThread);
            th.setDaemon(true);
            th.start();
            String to = "all";

            while (true) {
                String text = scanner.nextLine();
                if (user.getUserId().contains("Denied")) {
                    System.out.println("Access denied. Try  ~login");
                }
                if (text.contains("~help")) {
                    System.out.println("Some commands:\nexit ~exit \nto login ~login \nto logout ~logout \nchange to  ~to \n" +
                            "get list of logged users  ~getuserstatus \nlist of all users ~getallusers \ncreate and come in chartroom ~createroom" +
                            "\n~joinroom  \n~leaveroom \n~help  ");
                }
                if (text.contains("~exit")) {
                    try {
                        user.logOut();
                    } catch (IOException ioe) {
                    }
                    break;
                }
                if (text.contains("~getuserstatus")) {
                    try {
                        System.out.println("There are logged users: ");
                       user.getListUsers("logged");
                    } catch (IOException ioe) {
                    }

                }
                if(text.contains("~getallusers")){
                    try {
                        System.out.println("This is the list of users");
                        user.getListUsers("all");
                    } catch (IOException ioe) {
                    }
                }
                if (text.contains("~to")) {
                    if (user.isChatRoomMode()) {
                        System.out.println("You can send messages to only users are in chatroom");
                        continue;
                    }
                    System.out.println("Write logins for whom you want send messages (use \", \" to separate it. \"all\" or empty space- to send" +
                            " all users)");
                    to = scanner.nextLine();
                    System.out.println("OK. You`l send messages to " + to);
                }
                if (text.contains("~login")) {
                    if (!user.getUserId().contains("Denied")) {
                        System.out.println("You are logged in");
                        continue;
                    } else {
                        System.out.println("Enter login: ");
                        login = scanner.nextLine();
                        System.out.println("Enter password: ");
                        password = scanner.nextLine();
                        user.setLogin(login);
                        user.setPassword(password);

                        try {
                            user.logIn(login, password, "http://localhost:8080/login");
                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                        if (!user.getUserId().contains("Denied")) {
                            System.out.println("HTTP authorization: OK ");
                        }
                    }
                }
                if (text.contains("~logout")) {
                    System.out.println("Are you sure?  press Y for logout, or any other if you dont");
                    String answer = scanner.nextLine().toLowerCase();
                    if (answer.contains("y")) {

                        try {
                            Message m = new Message();
                            m.setText(login + " is out");
                            m.setFrom(login);
                            m.setTo("all");
                            m.send("http://localhost:8080/add", user.getUserId());
                            System.out.println(user.logOut());
                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                    }
                }


                if (text.contains("~createroom")) {
                    System.out.println("Enter the name of  the new chartroom you want to create:");
                    String name = scanner.nextLine();
                    user.toChartRoom(name);
                    System.out.println("You are in chartroom " + name);
                    to = name;
                    try {
                        Message m = new Message();
                        m.setText(login + " create new chartrooom " + name + "\n Join him!");
                        m.setFrom(login);
                        m.setTo("all");
                        m.send("http://localhost:8080/add", user.getUserId());
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
                if (text.contains("~joinroom")) {
                    System.out.println("Enter the room name you want to join");
                    String name = scanner.nextLine();
                    user.toChartRoom(name);
                    System.out.println("You are in chartroom " + name);
                    to = name;
                    try {
                        Message m = new Message();
                        m.setText(login + " join to chartrooom " + name);
                        m.setFrom(login);
                        m.setTo(name);
                        m.send("http://localhost:8080/add", user.getUserId());
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
                if (text.contains("~leaveroom")) {
                    user.fromChartRoom();
                    System.out.println("You are leave chart room");

                    try {
                        Message m = new Message();
                        m.setText(login + " is out");
                        m.setFrom(login);
                        m.setTo(user.getRoomName());
                        m.send("http://localhost:8080/add", user.getUserId());
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                    to = "all";
                }

                if (text.contains("~")) {
                    continue;
                }
                Message m = new Message();
                m.setText(text);
                m.setFrom(login);
                m.setTo(to);

                try {
                    int res = m.send("http://localhost:8080/add", user.getUserId());
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