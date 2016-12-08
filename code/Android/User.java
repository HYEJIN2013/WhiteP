package com.company;

import java.util.Date;

/**
 * Created by grote on 03.06.2016.
 */
public class User {

    public static final String SYSTEM_LOGIN_ADM = "adm";
    public static final String SYSTEM_LOGIN_ROOM = "room";

    private final String login;
    private String password;

    private Date activity;
    private String room;

    public User(String login, String password) {
        this.login = login;
        this.password = password;
    }

    public String getLogin() {
        return login;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getRoom() {
        return room;
    }

    public void setRoom(String room) {
        this.room = room;
    }

    public boolean isRoom(String rm) {

        if (isSystem()) return true;

        if (rm == room) return true;

        return rm != null && room != null
                && rm.trim().toLowerCase().equals(room.trim().toLowerCase());

    }

    public boolean isSystem() {
        return login.equals(SystemName.ADM.toString())
                || login.equals(SystemName.ROOM.toString());
    }

    public void updateActivity() {
        this.activity = new Date();
    }

    public void removeActivity() {
        this.activity = null;
    }

    public Status getStatus() {

        if (activity != null
                && (new Date().getTime() - activity.getTime()) <= Status.OFFLINE_TIME_OUT)

            return Status.ONLINE;
        else
            return Status.OFFLINE;
    }

    public enum Status {
        ONLINE, OFFLINE;

        private static final int OFFLINE_TIME_OUT = 2000;

        @Override
        public String toString() {
            return name().toLowerCase();
        }
    }

    public enum SystemName {
        ADM, ROOM;

        @Override
        public String toString() {
            return name().toLowerCase();
        }
    }
}
