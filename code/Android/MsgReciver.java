package main;

import java.io.DataInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.Socket;

public class MsgReciver extends Thread{
	
	Server se = new Server();
	InputStream is = null;
	DataInputStream dis = null;
	
	Socket s = null;
	
	public MsgReciver(String msg)
	{
		super(msg);
	}

	public void run()
	{
		//Receive messages from the client
		try {
			s = se.s;
			is = s.getInputStream();
			dis = new DataInputStream(is);	 //Message from the client
			String received_data = dis.readUTF(); //data that we receive from the client
			System.out.println(" Client: "+received_data);
			se.log.setText(se.log.getText()+" Client: "+received_data);
			//////	
		} catch (IOException e) {e.printStackTrace();}	 
	}
	
}
