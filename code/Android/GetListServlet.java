package com.company;

import java.io.IOException;
import java.io.OutputStream;
import java.util.Date;

import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

@WebServlet("/get")
public class GetListServlet extends HttpServlet {
	
	public void doGet(HttpServletRequest req, HttpServletResponse resp)
		throws IOException 
	{
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

        Date lastRead = (Date) session.getAttribute("last_read_date");

        User usr = UserList.getInstance().get(lgn);
        usr.updateActivity();

        String json = MessageList.getInstance().toJSON(usr, lastRead);
		if (json != null) {
			OutputStream os = resp.getOutputStream();
			os.write(json.getBytes());
		}

        session.setAttribute("last_read_date", lastRead);
	}
}
