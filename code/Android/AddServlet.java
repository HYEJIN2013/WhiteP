package com.company;

import java.io.IOException;
import java.io.InputStream;

import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

@WebServlet("/add")
public class AddServlet extends HttpServlet {
	
	public void doPost(HttpServletRequest req, HttpServletResponse resp)
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

		User sender = UserList.getInstance().get(lgn);
		sender.updateActivity();

		InputStream is = req.getInputStream();
		byte[] buf = new byte[req.getContentLength()];
		is.read(buf);

		Message msg = Message.fromJSON(new String(buf));
		if (msg != null) {

			processMessage(msg, sender);
		} else {
			resp.setStatus(400); // Bad request
		}
	}

	private void processMessage(Message msg, User sender) {

		msg.setFrom(sender.getLogin());
		msg.setRoom(sender.getRoom());

		if (!msg.isToAll()) {

			User receiver = UserList.getInstance().get(msg.getTo().trim().toLowerCase());
			if (receiver == null) {

				Message warning = Message.createAnswer("There is no receiver with a name \"" + msg.getTo().trim() + "\"!", msg);
				warning.setFrom(User.SystemName.ADM.toString());
				MessageList.getInstance().add(warning);
				return;

			} else if (!receiver.isRoom(sender.getRoom())) {

				Message warning = Message.createAnswer("There is no receiver in this room!", msg);
				warning.setFrom(User.SystemName.ADM.toString());
				MessageList.getInstance().add(warning);
				return;

			} else {
				msg.setTo(receiver.getLogin()); // with lower and upper case
			}
		}
		MessageList.getInstance().add(msg);

		processCmdMessage(msg, sender);
	}

	private void processCmdMessage(Message msg, User sender) {

		if (msg.isToAll()) return;

		String to = msg.getTo().trim().toLowerCase();
		if (to.equals(User.SystemName.ADM.toString())) {

			String cmd = msg.getText().trim().toLowerCase();
			if (cmd.equals("help")) {
				executeAdmHelp(msg);
			} else if (cmd.equals("users")) {
				executeAdmUsers(msg);
			} else if (cmd.equals("users in room")) {
				executeAdmUsersInRoom(msg, sender);
			} else if (cmd.equals("rooms")) {
				executeAdmRooms(msg);
			}
		} else if (to.equals(User.SystemName.ROOM.toString())) {

			String room = msg.getText().trim().toLowerCase();
			if (room.equals("exit")) {
				executeRoomExit(msg, sender);
			} else if (!room.isEmpty()) {
				executeRoomEnter(msg, sender, room);
			}
		}
	}

	private void executeAdmHelp(Message msg) {

		MessageList.getInstance().add(Message.createAnswer("#adm: help - this command", msg));
		MessageList.getInstance().add(Message.createAnswer("#adm: users - show all users with status", msg));
		MessageList.getInstance().add(Message.createAnswer("#adm: rooms - show all rooms", msg));
		MessageList.getInstance().add(Message.createAnswer("#room: room_name - enter in the room (create a new if necessary)", msg));
		MessageList.getInstance().add(Message.createAnswer("#room: exit - escape to global chat", msg));
	}

	private void executeAdmUsers(Message msg) {

		MessageList.getInstance().add(Message.createAnswer("There are all users:", msg));

		for (User u : UserList.getInstance().getUsers()) {
			MessageList.getInstance().add(Message.createAnswer(u.getLogin() + ", status: " + u.getStatus(), msg));
		}
	}

	private void executeAdmUsersInRoom(Message msg, User sender) {
		
		MessageList.getInstance().add(Message.createAnswer("There are users in this room:", msg));

		for (User u : UserList.getInstance().getUsers()) {
            if (u.isRoom(sender.getRoom())) {
                MessageList.getInstance().add(Message.createAnswer(u.getLogin() + ", status: " + u.getStatus(), msg));
            }
        }
	}

	private void executeAdmRooms(Message msg) {

		MessageList.getInstance().add(Message.createAnswer("There are all rooms:", msg));

		for (String r : RoomList.getInstance().getNameList()) {
			MessageList.getInstance().add(Message.createAnswer(r, msg));
		}
	}
	
	private void executeRoomExit(Message msg, User sender) {

		sender.setRoom(null);

		Message answer = Message.createAnswer("Now you in a global chat", msg);
		answer.setFrom(User.SystemName.ADM.toString());
		answer.setRoom(null);
		MessageList.getInstance().add(answer);
	}

	private void executeRoomEnter(Message msg, User sender, String room) {

		String foundRoom = RoomList.getInstance().get(room);
		if (foundRoom == null) {

			RoomList.getInstance().add(room, msg.getText().trim());
			sender.setRoom(msg.getText().trim());
		} else {
			sender.setRoom(foundRoom);
		}

		Message answer = Message.createAnswer("Now you in the room \"" + sender.getRoom() + "\"", msg);
		answer.setFrom(User.SystemName.ADM.toString());
		answer.setRoom(sender.getRoom());
		MessageList.getInstance().add(answer);
	}
}
