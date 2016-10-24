package server;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.InetSocketAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Date;
import org.json.simple.JSONObject;
 
public class ServerWork {
    private ServerSocket serverSocket;
    private Socket socket;
    private File file;
    ObjectInputStream ois = null;
    ObjectOutputStream oos = null;
 
    public ServerWork() throws IOException{
        serverSocket = new ServerSocket(5001);
        socket = new Socket();
        file = new File("serverMessage.txt");
    }
 
    /**[Server]연결대기 상태 */
    public void listening() throws IOException{
        System.out.println("[연결 기다림]");
        socket = serverSocket.accept();    
        InetSocketAddress isa = (InetSocketAddress) socket.getRemoteSocketAddress();
        System.out.println("[연결 수락함]" + isa.getHostName());
    }
 
    /**[Server]메시지 받기 */
    public String receiveMessageFromClient() throws IOException, ClassNotFoundException{
        String m = "";
        ois = new ObjectInputStream(socket.getInputStream());
        m = ois.readObject().toString();
        System.out.println("[데이터 받기 성공]: " +m);
        return m;
    }
 
    /**[Server]메시지 보내기 */
    public void sendMessageToClient()  throws IOException {
        BufferedReader brForWrite = new BufferedReader(new InputStreamReader(System.in));
        JSONObject jsonObj = new JSONObject();
        jsonObj.put("이름", "서버");
        jsonObj.put("아이피", socket.getLocalAddress());
        jsonObj.put("포트", socket.getLocalPort());
        jsonObj.put("보낸 시간", new Date().toString());
        jsonObj.put("메시지", brForWrite.readLine());
 
        FileWriter fw = new FileWriter(file, true);
        fw.write(jsonObj.toJSONString()+"\r\n");
 
        oos = new ObjectOutputStream(socket.getOutputStream());
        oos.writeObject(jsonObj.toJSONString());
        System.out.println("[클라이언트에 데이터 보내기 성공]");
 
        fw.close();
    }
    
    /**[Server]입출력스트림 및 소켓 종료*/
    public void closeConnection() throws IOException{
        if(ois != null) ois.close();
        if(oos != null) oos.close();
        if(!socket.isClosed()) socket.close();
        System.out.println("[연결종료]");
    }
 
    /**[Server]서버소켓 종료 */
    public void closeServerSocket() throws IOException{
        if(!serverSocket.isClosed()){
            serverSocket.close();
        }
    }
}