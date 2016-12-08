import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class AddServlet extends HttpServlet {

    private MessageList msgList = MessageList.getInstance();

    public void doPost(HttpServletRequest req, HttpServletResponse resp)
            throws IOException {
        String id = req.getHeader("id").replace("id=", "");
        if (Users.usersId.containsValue(id)) {
            BufferedReader bf = new BufferedReader(new InputStreamReader(req.getInputStream()));
            Message msg = Message.fromJSON(bf.readLine());
            if (msg != null) {
                msgList.add(msg);
            } else {
                resp.setStatus(400);
            } // Bad request
            bf.close();
        }
    }
}
