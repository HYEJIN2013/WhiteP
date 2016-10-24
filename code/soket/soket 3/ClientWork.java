package client;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.util.Date;
import org.json.simple.JSONObject;
 
public class ClientWork {
    private Socket socket;
    private File file;
    ObjectOutputStream oos = null;
    ObjectInputStream ois = null;
 
    public ClientWork() {
        socket = new Socket();
        file = new File("clientMessage.txt");
    }
 
    /**[Client]연결요청 */
    public void connectingWithServer() throws IOException{
        System.out.println("[연결 요청]");
        socket.connect(new InetSocketAddress("localhost", 5001));
        System.out.println("[연결 성공]");
    }
 
    /**[Client]메시지 보내기 */
    public boolean sendMessageToServer() throws IOException{
        BufferedReader brForWrite = new BufferedReader(new InputStreamReader(System.in));
        JSONObject jsonObj = new JSONObject();
        String inputMessage = brForWrite.readLine();
 
        jsonObj.put("이름", "클라");
        jsonObj.put("아이피", socket.getLocalAddress());
        jsonObj.put("포트", socket.getLocalPort());
        jsonObj.put("보낸 시간", new Date().toString());
        jsonObj.put("메시지", inputMessage);
 
        oos = new ObjectOutputStream(socket.getOutputStream());
        
        if(inputMessage.toString().equals("0")){
            System.out.println("[클라이언트 종료]");
            oos.writeObject("0");
            return false;
        } else{
            FileWriter fw = new FileWriter(file, true);
            fw.write(jsonObj.toJSONString()+"\r\n");
 
            oos.writeObject(jsonObj.toJSONString());
            System.out.println("[서버에 데이터 보내기 성공]");
            fw.close();
            return true;
        }
    }
    
    
    /**[Client]메시지 받기 */
    public String receiveMessageFromServer() throws IOException, ClassNotFoundException{
        String m = "";
        ois = new ObjectInputStream(socket.getInputStream());
        m = "[데이터 받기 성공]: " + ois.readObject().toString();
        return m;
    }
 
    /**[Client]입출력스트림 및 소켓 종료*/
    public void closeConnection() throws IOException{
        if(ois != null) ois.close();
        if(oos != null) oos.close();
        if(!socket.isClosed()) socket.close();
        System.out.println("[연결 종료]");
    }
}