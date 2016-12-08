package ua.kiev.prog;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

/**
 * Created by Oleg on 02.08.2016.
 */
public class UserList {
    private final HashMap<String, String> list = new HashMap<>();

    private static final UserList userList = new UserList();

    public static UserList getInstance() {
        return userList;
    }

    private UserList() {
    }

    public synchronized void add(String user, String status) {
        list.put(user, status);
    }

    public synchronized void changeStatus(String user, String status) {

        list.replace(user, status);
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder("User List:");
        sb.append(System.lineSeparator());
        list.entrySet().stream().forEach(n -> sb.append("Login: ").append(n.getKey()).append(" - ").append(n.getValue()).append(System.lineSeparator()));
        return sb.toString();
    }
    //    public synchronized String toJSON(int n) {
//        List<Message> res = new ArrayList<Message>();
//        for (int i = n; i < list.size(); i++)
//            res.add(list.get(i));
//
//        if (res.size() > 0) {
//            Gson gson = new GsonBuilder().create();
//            return gson.toJson(res.toArray());
//        } else
//            return null;
//    }
}
