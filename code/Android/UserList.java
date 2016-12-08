package com.company;

import java.util.Collection;
import java.util.HashMap;

/**
 * Created by grote on 03.06.2016.
 */
public class UserList {

    private UserList() {}
    private static final UserList INSTANCE = new UserList();
    public static UserList getInstance() {return INSTANCE;}

    private HashMap<String, User> map = new HashMap<>();

    public void add(User value) {
        map.put(value.getLogin(), value);
    }

    public User get(String key) {
        return map.get(key);
    }

    public Collection<User> getUsers() {
        return map.values();
    }

    {
        add(new User(User.SystemName.ADM.toString(), "psw" + User.SystemName.ADM.toString()));
        add(new User(User.SystemName.ROOM.toString(), "psw" + User.SystemName.ROOM.toString()));
        add(new User("usr1", "psw1"));
        add(new User("usr2", "psw2"));
        add(new User("usr3", "psw3"));
        add(new User("usr4", "psw4"));
    }
}
