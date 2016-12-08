package com.company;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.io.IOException;
import java.util.Date;

/**
 * Created by grote on 31.05.2016.
 */
@WebServlet("/login")
public class LoginServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {

        String lgn = req.getParameter("lgn").trim().toLowerCase();
        String psw = req.getParameter("psw");

        User user = UserList.getInstance().get(lgn);
        if (user == null || user.getPassword() == null || !user.getPassword().equals(psw)) {
            resp.setStatus(HttpServletResponse.SC_UNAUTHORIZED); // 401
            return;
        }

        HttpSession session = req.getSession(true);
        session.setAttribute("user_login", lgn);
        session.setAttribute("last_read_date", new Date());
        user.updateActivity();
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {

        if (req.getParameter("do").equals("logout"))
            return;

        HttpSession session = req.getSession(false);
        if (session == null) {
            resp.setStatus(HttpServletResponse.SC_UNAUTHORIZED); // 401
            return;
        }

        String lgn = (String) session.getAttribute("user_login");
        if (lgn == null) {
            resp.setStatus(HttpServletResponse.SC_UNAUTHORIZED); // 401
            return;
        }

        User user = UserList.getInstance().get(lgn);
        if (user != null) {
            user.removeActivity();
        }

        session.removeAttribute("user_login");
    }
}
