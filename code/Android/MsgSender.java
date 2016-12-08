package main;

import main.Client;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.PrintStream;
import java.net.ServerSocket;
import java.net.Socket;

public class MsgSender extends Thread{
	Client c = new Client();
	ServerSocket ss = null;
	Socket s = null;
	OutputStream os = null;
	DataOutputStream dos = null;
	
	PrintStream output;
	
	InputStream is = null;
	DataInputStream dis = null;
	
	public MsgSender(String msg)
	{
		super(msg);
	}
	
	public void run()
	{
		try {
			s=c.s;
			output = new PrintStream(s.getOutputStream());
			output.println(c.msg.getText());
			c.log.setText(c.log.getText()+" Me: "+c.msg.getText());
			c.msg.setText("");
		} catch (IOException e) {e.printStackTrace();}
	}
}