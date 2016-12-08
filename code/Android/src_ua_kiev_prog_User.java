package ua.kiev.prog;

/**
 * Created by Oleg on 02.08.2016.
 */
public class User {
    private String login;
    private String status;

    public User(String login, String status) {
        login = login;
        status = status;
    }

    public User() {
    }

    public String getLogin() {
        return login;
    }

    public void setLogin(String login) {
        login = login;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        status = status;
    }

    @Override
    public String toString() {
        return "User: " + login + " - " + status;
    }
}
