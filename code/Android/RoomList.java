package com.company;

import java.util.Collection;
import java.util.HashMap;

/**
 * Created by grote on 04.06.2016.
 */
public class RoomList {

    private RoomList() {}
    private static RoomList INSTANCE = new RoomList();
    public static RoomList getInstance() {return INSTANCE;}

    private HashMap<String, String> map = new HashMap<>();

    public void add(String key, String value) {
        map.put(key, value);
    }

    public String get(String key) {
        return map.get(key);
    }

    public Collection<String> getNameList() {
        return map.values();
    }
}
