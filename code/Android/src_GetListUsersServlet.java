import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.OutputStream;

public class GetListUsersServlet extends HttpServlet {


    public void doGet(HttpServletRequest req, HttpServletResponse resp)
            throws IOException {

        String id = req.getHeader("id").replace("id=", "");
        if (Users.usersId.containsValue(id)) {
            Gson gson = new GsonBuilder().create();
            String json;
            if (req.getHeader("option").contains("all")) {
                json = gson.toJson(Users.getUsers());
            } else {
                json = gson.toJson(Users.getLoggedUsers());
            }


            if (json != null) {
                OutputStream os = resp.getOutputStream();
                os.write(json.getBytes());
            }
        }

    }
}