package homework11.serverSysInfo;

import java.io.*;
import java.net.*;

public class Client implements Runnable {

	private Socket socket;
	private String answer;
	Thread t;

	public Client(Socket socket, String answer) {

		super();
		this.socket = socket;
		this.answer = answer;
		t = new Thread(this);
		t.start();
	}

	@Override
	public void run() {

		try (InputStream is = socket.getInputStream();
				OutputStream os = socket.getOutputStream();
				PrintWriter pw = new PrintWriter(os)) {

			byte[] rec1 = new byte[is.available()];
			is.read(rec1);
			String response = "HTTP/1.1 200 OK\r\n" + "Server: My_Server\r\n" + "Content-Type: text/html\r\n"
					+ "Content-Length: " + "\r\n" + "Connection: close\r\n\r\n";
			pw.print(response + answer);
			pw.flush();

		} catch (IOException e) {
			System.out.println(e.toString());
		}
	}
}
