package main;

import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.net.*;
import java.io.*;

import javax.swing.*;

@SuppressWarnings("serial")
public class Server extends JFrame implements ActionListener{

	
	ServerSocket ss = null;
	Socket s = null;
	OutputStream os = null;
	DataOutputStream dos = null;
	
	InputStream is = null;
	DataInputStream dis = null;
	
	int port = 9000;
	boolean isOn=false;
	
	JTextField portTxt,msg;
	JLabel infoPort;
	static JTextArea log;
	JButton send,start;
	JScrollPane scrollBar;
	
	public Server()
	{
		setLayout(null);
		
		portTxt = new JTextField("9000");
		msg = new JTextField();
		setLog(new JTextArea(5,20));
		infoPort = new JLabel("Port:");
		send = new JButton("SEND");
		start = new JButton("Start Server");
		scrollBar = new JScrollPane(log);
		
		portTxt.setBounds(250, 10, 60, 25);
		msg.setBounds(10, 540, 340, 25);
		log.setBounds(10, 45, 395, 485);
		infoPort.setBounds(210, 10, 50, 25);
		send.setBounds(360, 540, 80, 25);
		start.setBounds(320, 10, 120, 25);
		scrollBar.setBounds(415, 45, 25, 485);
		
		//log.setColumns(20);
		//log.setRows(5);
		log.setText("Chat:\n");
		//scrollBar.setPreferredSize(new Dimension(395,485));
		send.addActionListener(this);
		start.addActionListener(this);
		
		add(portTxt);
		add(msg);
		add(getLog());
		add(infoPort);
		add(send);
		add(start);
		add(scrollBar, BorderLayout.CENTER);
		
	}
	
	public static void main(String[] args) {
		
		Server server = new Server();
		server.setVisible(true);
		server.setSize(450, 600);
		server.setResizable(false);
		server.setDefaultCloseOperation(EXIT_ON_CLOSE);
		server.setTitle("Server Chat");

	}

	public void start(int port) {
		
		

		try{
			ss = new ServerSocket(port);  //Start the server in the port specified by the user
			s= ss.accept();
			log.setText(log.getText()+"serverOK");

			Thread MsgSender = new MsgSender(" THREAD ");
			Thread MsgReciver = new MsgReciver(" THREAD 2");
			
			MsgSender.start();
			MsgReciver.start();
			log.setText(log.getText()+"afterthreadOK");
		}catch(Exception ex){ex.printStackTrace();}
		
	}


	@Override
	public void actionPerformed(ActionEvent e) {
		//Send messages to the client
		if(e.getSource()==send)
		{
			Thread MsgSender = new MsgSender(" THREAD ");
			MsgSender.start();
			//dos.writeUTF(msg.getText());
			//getLog().setText(getLog().getText()+" Server: "+msg.getText());
		}		
		//Start/Stop the server
		if(e.getSource()==start&&isOn==false)
		{
			
			isOn = true;
			start.setText("Stop Server");
			port = Integer.parseInt(portTxt.getText());
			
			log.setText("botonOK");
			
			start(port);
		}else if(e.getSource()==start&&isOn==true)
		{
			isOn = false;
			start.setText("Start Server");
			try {
				ss.close();
				s.close();
				os.close();
				dos.close();
			} catch (IOException e1) {e1.printStackTrace();}
		}
		
	}

	public JTextArea getLog() {
		return log;
	}

	public static void setLog(JTextArea log) {
		Server.log = log;
	}

}
