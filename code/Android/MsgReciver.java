package main;

import java.io.DataInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.Socket;

public class MsgReciver extends Thread{
	
	Client c = new Client();
	InputStream is = null;
	DataInputStream dis = null;
	
	Socket s = null;
	
	public MsgReciver(String msg)
	{
		super(msg);
	}

	public void run()
	{
		//Receive messages from the server
		try {
			s=c.s;
			is = s.getInputStream();
			dis = new DataInputStream(is);	 //Message from the server 
			String received_data = dis.readUTF();  //data that we receive from the server
			System.out.println(" Server: "+received_data);
			c.log.setText(c.log.getText()+" Server: "+received_data);
		
		} catch (IOException e) {e.printStackTrace();}	 
	}
	
}