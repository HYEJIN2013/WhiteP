package tiy.networking;

import java.text.SimpleDateFormat;

/**
 * Created by Corey Shaw on 4/28/2016.
 */
public class Message {

    public String text;
    public String name;
    public String date = new SimpleDateFormat("EEE hh:m a").format(new java.util.Date());

    public Message (String user, String text ){
this.name = user;
    this.text = text;
}
    @Override
    public String toString() {
        String finalString = (name+" "+text+" Sent on "+ date + "sent on"+ date );
        return finalString;

    }

}