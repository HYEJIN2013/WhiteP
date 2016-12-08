package ua.kiev.prog;

import java.util.ArrayList;
import java.util.List;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

public class MessageList {

    private static final MessageList msgList = new MessageList();

    private final List<Message> list = new ArrayList<Message>();

    public static MessageList getInstance() {
        return msgList;
    }

    private MessageList() {
    }

    public synchronized void add(Message m) {
        list.add(m);
    }

    public synchronized String toJSON(int n, String login, String room) {
        List<Message> res = new ArrayList<Message>();

        for (int i = n; i < list.size(); i++)
            if (list.get(i).getFrom().equals(login) || list.get(i).getTo().equals(login) || (list.get(i).getTo().equals("all") && list.get(i).getRoom().isEmpty()) || (list.get(i).getTo().equals("all") && list.get(i).getRoom().equals(room))) {
                res.add(list.get(i));
            }

        if (res.size() > 0) {
            Gson gson = new GsonBuilder().create();
            return gson.toJson(res.toArray());
        } else
            return null;
    }
}
