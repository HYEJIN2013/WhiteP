package main;

import main.Server;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.ServerSocket;
import java.net.Socket;

public class MsgSender extends Thread{
	Server se = new Server();
	ServerSocket ss = null;
	Socket s = null;
	OutputStream os = null;
	DataOutputStream dos = null;
	
	InputStream is = null;
	DataInputStream dis = null;
	
	public MsgSender(String msg)
	{
		super(msg);
	}
	
	public void run()
	{
		try {
			s = se.s;
			os = s.getOutputStream();	//What we send
			dos = new DataOutputStream(os);    //What we use to send the output data(os)
			dos.writeUTF("You have connected to the main server");
		} catch (IOException e) {e.printStackTrace();}
		
		
	}
	
}