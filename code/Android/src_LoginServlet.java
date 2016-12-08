import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;
import java.net.HttpCookie;

/**
 * Created by Nick on 05.08.2016.
 */
public class LoginServlet extends HttpServlet {
    public void doPost(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        String[] msg = req.getHeader("Cookie").split("&");
        String login = msg[0];
        String password = msg[1];
        String ms = "Denied";
        try{if(!Users.usersId.containsKey(login)){//single-mode access by 1 account
       try {
           if(Users.cred.get(login).equals(password)) {//pass checking
               ms = Users.addUsersId(login);
           }
       }catch (Exception e){}}}catch (Exception e){}



        Cookie cook = new Cookie("id", ms);
        resp.addCookie(cook);
    }
}
