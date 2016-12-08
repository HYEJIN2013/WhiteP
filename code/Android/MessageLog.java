package tiy.networking;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by Tisha868 on 5/3/16.
 */
public class MessageLog { // container class
    public ArrayList<Message> messageItems = new ArrayList<Message>(); /// delcared in GLobal scoop

    public MessageLog(Message incomingIM) { //
        messageItems.add(incomingIM); //
    }

    public MessageLog() {

    }
}
