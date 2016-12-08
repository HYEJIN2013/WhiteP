import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import javax.servlet.http.Cookie;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

/**
 * Created by Nick on 05.08.2016.
 */
public class User {
    private String login;
    private String password;
    private boolean isLogged;
    private String userId = "0";
    private String userStatus = "not with us";
    private boolean chatRoomMode;

    public boolean isChatRoomMode() {
        return chatRoomMode;
    }

    private ChatRoom chatRoom;

    public String getRoomName() {
        return this.chatRoom.getChrName();
    }

    public void toChartRoom(String chrName) {
        this.chatRoom = new ChatRoom(chrName);
        chatRoomMode = true;


    }

    public void fromChartRoom() {
        chatRoomMode = false;

    }

    public void setChatRoomMode(boolean chatRoomMode) {
        this.chatRoomMode = chatRoomMode;
    }


    public User(String login, String password) {
        this.login = login;
        this.password = password;
    }

    public String getLogin() {
        return login;
    }

    public void setLogin(String login) {
        this.login = login;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public boolean isLogged() {
        return isLogged;
    }

    public void setLogged(boolean logged) {
        isLogged = logged;
    }

    public String getUserId() {
        return userId;
    }

    public void setUserId(String userId) {
        this.userId = userId;
    }

    public String logIn(String login, String password, String url) throws IOException {
        URL obj = new URL(url);
        HttpURLConnection conn = (HttpURLConnection) obj.openConnection();
        String myCookie = login + "&" + password;
        conn.setRequestProperty("Cookie", myCookie);
        conn.setRequestMethod("POST");
        conn.connect();
        String id = conn.getHeaderField("Set-Cookie");
        setUserId(id);
        conn.disconnect();
        return id;
    }

    public String logOut() throws IOException {
        URL obj = new URL("http://localhost:8080/logout");
        HttpURLConnection conn = (HttpURLConnection) obj.openConnection();
        conn.setRequestProperty("login", this.login);
        conn.setRequestMethod("GET");
        conn.connect();
        String response;
        response = conn.getHeaderField("Set-Cookie");
        if (response.contains("logout")) {
            setUserId("Denied");
        }
        conn.disconnect();
        return response;
    }

    public void getListUsers(String option) throws IOException {
        URL url = new URL("http://localhost:8080/getlistusers");
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();

        conn.setRequestProperty("id", userId);
        if(option.equals("all")){
        conn.setRequestProperty("option","all");}else{
            conn.setRequestProperty("option","logged");
        }
        conn.setRequestMethod("GET");
        conn.connect();
        InputStream is = conn.getInputStream();


        try {
            int sz = is.available();
            if (sz > 0) {


                Gson gson = new GsonBuilder().create();
                String[] list = gson.fromJson(new BufferedReader(new InputStreamReader(is)), String[].class);

                for (String m : list) {

                    System.out.println(m);

                }
            }
        } finally {
            is.close();
        }

    }
}
