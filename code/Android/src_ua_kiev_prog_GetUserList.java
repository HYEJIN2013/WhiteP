package ua.kiev.prog;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.io.IOException;
import java.io.InputStream;

/**
 * Created by Oleg on 02.08.2016.
 */
public class GetUserList extends HttpServlet {

    private MessageList msgList = MessageList.getInstance();
    private UserList userList = UserList.getInstance();

    public void doPost(HttpServletRequest req, HttpServletResponse resp)
            throws IOException {


        InputStream is = req.getInputStream();
        byte[] buf = new byte[req.getContentLength()];
        is.read(buf);


        Message msg = Message.fromJSON(new String(buf));


        msg.setTo(msg.getFrom());
        msg.setFrom("Server");
        msg.setText(userList.toString());
        System.out.println(msg);

        msgList.add(msg);

    }
}
