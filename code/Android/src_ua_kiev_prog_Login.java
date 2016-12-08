package ua.kiev.prog;

import java.io.IOException;
import java.io.InputStream;
import java.util.HashMap;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

public class Login extends HttpServlet {
    private HashMap<String, String> LogPass = new HashMap<>();
    private MessageList msgList = MessageList.getInstance();
    private UserList userList = UserList.getInstance();

    public void doPost(HttpServletRequest req, HttpServletResponse resp)
            throws IOException {
        LogPass.put("user1", "user1");
        LogPass.put("user2", "user2");
        LogPass.put("user3", "user3");
        LogPass.put("Oleg", "pass");


        InputStream is = req.getInputStream();
        byte[] buf = new byte[req.getContentLength()];
        is.read(buf);

        Message msg = Message.fromJSON(new String(buf));


        if (LogPass.get(msg.getFrom()).equals(msg.getTo())) {
            resp.setStatus(200);
//            HttpSession session = req.getSession(true);
//            session.setAttribute("login", msg.getFrom());
            userList.add(msg.getFrom(), "active");

        } else {
            resp.setStatus(400); // Bad request
        }

    }

}
