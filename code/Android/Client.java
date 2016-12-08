package main;

import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.net.*;
import java.io.*;

import javax.swing.*;

@SuppressWarnings("serial")
public class Client extends JFrame implements ActionListener{

	
	Socket s = null;
	InputStream is = null;
	DataInputStream dis = null;
	
	int port=9000;
	String ip="localhost";
	
	PrintStream outPut;
	BufferedReader input,keyboard;
	
	boolean isOn=false;
	
	JTextField portTxt,ipTxt,msg;
	JLabel infoPort,infoIp;
	static JTextArea log;
	JButton send,start;
	JScrollPane scrollBar;
	
	public Client()
	{
		setLayout(null);
		
		portTxt = new JTextField("9000");
		ipTxt = new JTextField("localhost");
		infoIp = new JLabel("IP:");
		msg = new JTextField();
		log = new JTextArea(5,20);
		infoPort = new JLabel("Port:");
		send = new JButton("SEND");
		start = new JButton("Connect to Server");
		scrollBar = new JScrollPane(log);
		
		portTxt.setBounds(250, 10, 60, 25);
		ipTxt.setBounds(120, 10, 80, 25);
		infoIp.setBounds(95, 10, 20, 25);
		msg.setBounds(10, 540, 340, 25);
		log.setBounds(10, 45, 395, 485);
		infoPort.setBounds(210, 10, 50, 25);
		send.setBounds(360, 540, 80, 25);
		start.setBounds(320, 10, 120, 25);
		scrollBar.setBounds(415, 45, 25, 485);
		
		log.setText("Chat:\n");
		scrollBar.setPreferredSize(new Dimension(395,485));
		send.addActionListener(this);
		start.addActionListener(this);
		
		add(infoIp);
		add(ipTxt);
		add(portTxt);
		add(msg);
		add(log);
		add(infoPort);
		add(send);
		add(start);
		add(scrollBar, BorderLayout.CENTER);
		
	}
	
	public static void main(String[] args) {
		
		Client client = new Client();
		client.setVisible(true);
		client.setSize(450, 600);
		client.setResizable(false);
		client.setDefaultCloseOperation(EXIT_ON_CLOSE);
		client.setTitle("Client Chat");

	}
	
	public void read(String ip,int port)
	{
		try{
			s = new Socket(ip,port);	 //Start a connection with a server with an ip and a port specified
			
			Thread MsgSender = new MsgSender(" THREAD ");
			Thread MsgReciver = new MsgReciver(" THREAD 2");
			
			MsgSender.start();
			MsgReciver.start();
				
			}catch(Exception ex)
				{
				log.setText("Couldn't connect to the server: "+ ip + "with the port:"+port);
				System.out.println("Couldn't connect to the server: "+ ip + "with the port:"+port);
				}
	}


	@Override
	public void actionPerformed(ActionEvent e) {
		//CONNECT TO THE SERVER
		if(e.getSource()==start)
		{
			int port = Integer.parseInt(portTxt.getText());
			String ip = ipTxt.getText();
			read(ip,port);
		}
		//SEND MESSAGES TO THE CLIENT
		if(e.getSource()==send)
		{
			//outPut = new PrintStream(s.getOutputStream());
			//outPut.println(msg.getText());			
			Thread MsgSender = new MsgSender(" THREAD ");

			MsgSender.start();
			
		}
		
	}

	public JTextArea getLog() {
		return log;
	}

	public static void setLog(JTextArea log) {
		Client.log = log;
	}

}
