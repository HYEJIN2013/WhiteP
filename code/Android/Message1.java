package tiy.networking;

/**
 * Created by Tisha868 on 5/2/16.
 */
public class Message {  // message constructor
    public String clientName; // field clientName
    public String clientMessage;
    public String clientTimeStamp;

    public Message(String incomingMessage, String clientName, String clientTimeStamp) { // passing a string parameter
        // called incomingMessage,,.

        this.clientMessage = incomingMessage; // this constructor passing parameters
        this.clientName = clientName; //
        this.clientTimeStamp = clientTimeStamp;//
    }

    public Message() { // deffault constructor

    }

    @Override
    public String toString() {
        String history = ("message => " + this.clientMessage + " from " + this.clientName + " @ " + this
                .clientTimeStamp);

        return history;
    }
}