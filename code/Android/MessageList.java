package com.company;

import java.util.*;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

public class MessageList {

    private MessageList() {}
    private static final MessageList INSTANCE = new MessageList();
    public static MessageList getInstance() {return INSTANCE;}

    private final List<Message> list = new ArrayList<>();

    public synchronized void add(Message m) {
        m.setCurrentDate(); // add in date order
        list.add(m); // list must be sorted by date
    }

    public synchronized String toJSON(User receiver, Date lastRead) {

        List<Message> res = new ArrayList<>();

        long curTime = new Date().getTime();
        long lastTime = lastRead.getTime();

        // list must be sorted by date
        for (int i = list.size() - 1; i >= 0; i--) {

            Message msg = list.get(i);

            long msgTime = msg.getDate().getTime();
            if (lastTime >= msgTime) break;
            if (curTime <= msgTime) continue; // messages in last second aren`t added, becous it can be added in last second

            if (msg.isSend(receiver.getLogin(), receiver.getRoom())) res.add(msg);
        }
        Collections.reverse(res); // back in order by date

        lastRead.setTime(curTime - 1);

        if (res.size() > 0) {
            Gson gson = new GsonBuilder().create();
            return gson.toJson(res.toArray());
        } else {
            return null;
        }

    }
}
