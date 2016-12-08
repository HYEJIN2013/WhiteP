package com.company;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.text.SimpleDateFormat;
import java.util.Date;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

public class Message {

	private static final String TO_ALL = "ALL";
	private static final SimpleDateFormat dataFormat = new SimpleDateFormat("dd.MM.yyyy HH:mm:ss");

	public static Message createAnswer(String text, Message query) {
		Message answ = new Message(text);
		answ.setFrom(query.getTo());
		answ.setTo(query.getFrom());
		answ.setRoom(query.getRoom());
		return answ;
	}

	private Date date;
	private String from;
	private String to;
	private String text;
	private String room;

	public Message() {}

	public Message(String text) {
		setText(text);
	}

	public String toJSON() {
		Gson gson = new GsonBuilder().create();
		return gson.toJson(this);
	}

	public static Message fromJSON(String s) {
		Gson gson = new GsonBuilder().create();
		return gson.fromJson(s, Message.class);
	}

	@Override
	public String toString() {

		StringBuilder sb = new StringBuilder().append("[").append(dataFormat.format(date));
		if (!isGlobalRoom()) sb.append(", Room: ").append(room);
		sb.append(", From: ").append(from).append(", To: ").append((isToAll()) ? TO_ALL : to);
		sb.append("] ").append(text);

		return sb.toString();
	}

	public int send(String url, String cookies) throws IOException {

		URL obj = new URL(url);
		HttpURLConnection con = (HttpURLConnection) obj.openConnection();

		con.setRequestMethod("POST");
		con.setRequestProperty("Cookie", cookies);

		con.setDoOutput(true);
		try (OutputStream os = con.getOutputStream()) {
			os.write(toJSON().getBytes());
		}
		return con.getResponseCode();
	}

	public Date getDate() {
		return date;
	}

	public void setCurrentDate() {
		this.date = new Date();
	}

	public String getFrom() {
		return from;
	}

	public void setFrom(String from) {
		this.from = from;
	}

	public String getTo() {
		return to;
	}

	public void setTo(String to) {
		this.to = to;
	}

	public String getText() {
		return text;
	}

	public void setText(String text) {
		this.text = text;
	}

	public String getRoom() {
		return room;
	}

	public void setRoom(String room) {
		this.room = room;
	}

	public boolean isSend(String rc, String rm) {

		return isSendToReceiver(rc) && isSendToRoom(rm);
	}

	private boolean isSendToReceiver(String rc) {

		if (isToAll()) return true;

		String r = rc.trim().toLowerCase();
		if (r.equals(to.trim().toLowerCase()) || r.equals(from.trim().toLowerCase())) return true;

		return false;
	}

	private boolean isSendToRoom(String rm) {

		if (rm == room) return true;

		return rm != null && room != null
				&& rm.trim().toLowerCase().equals(room.trim().toLowerCase());
	}

	public boolean isToAll() {

		if (to == null) return true;

		String to_ = to.trim().toLowerCase();
		if (to_.isEmpty() || to_.equals(TO_ALL.toLowerCase())) return true;

		return false;
	}

	public boolean isGlobalRoom() {

		return room == null || room.trim().isEmpty();
	}
}
