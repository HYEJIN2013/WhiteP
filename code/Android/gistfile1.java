FROM MAIN BACKGROUND CLASS:
public void checkForNewMessages(){
        if(serverCreated){
            //*check for clients thread
            ServerCheckClientsThread serverClients = new ServerCheckClientsThread(server);
            serverClients.start();
            //*thread to check for new messages coming from clients
            ServerCheckMessagesThread serverMessages= new ServerCheckMessagesThread(server);
            serverMessages.start();
        }
        //*thread to check for messages coming from server to client
        ClientCheckMessagesThread clientMessages = new ClientCheckMessagesThread(clientFrame);
        clientMessages.start();
    }

OTHER 3 CLASSES:
public class ServerCheckMessagesThread extends Thread{
    ChatServer server;
    public ServerCheckMessagesThread(ChatServer inServer){
        server=inServer;
    }
    public void run(){
        try{
            while(true){
                server.checkForMessages();
            }
        }catch(Exception e){
            System.out.println("Error checking from new messages in ServerCheckMessagesThread");
        }
    }
}
public class ServerCheckClientsThread extends Thread{
    ChatServer server;
    public ServerCheckClientsThread(ChatServer inServer){
        server=inServer;
    }
    public void run(){
        try{
            int i=1;
            while(true){
                server.checkForClients(i);
                i++;
            }
        }catch(Exception e){
            System.out.println("Error in server checking for clients thread");
        }
    }
}
public class ClientCheckMessagesThread extends Thread{
    ClientFrame client;
    public ClientCheckMessagesThread(ClientFrame clientFrame){
        client=clientFrame;
    }
    public void run(){
        try{
            while(true){
                client.checkForMessages();
            }
        }catch(Exception e){
            System.out.println("Error checking for messages in ClientCheckMessagesThread");
        }
    }
}
