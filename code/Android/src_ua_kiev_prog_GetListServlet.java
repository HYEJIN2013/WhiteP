package ua.kiev.prog;

import java.io.IOException;
import java.io.OutputStream;
import java.util.List;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

public class GetListServlet extends HttpServlet {

    private MessageList msgList = MessageList.getInstance();

    public void doGet(HttpServletRequest req, HttpServletResponse resp)
            throws IOException {


        String fromStr = req.getParameter("from");
        int from = Integer.parseInt(fromStr);
        String login = req.getParameter("login");
        String room = req.getParameter("room");



        String json = msgList.toJSON(from, login, room);
        if (json != null) {
            OutputStream os = resp.getOutputStream();
            os.write(json.getBytes());
        }
    }
}
