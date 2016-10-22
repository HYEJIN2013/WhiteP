package sandbox;

import java.util.Properties;

import javax.mail.Message;
import javax.mail.MessagingException;
import javax.mail.Session;
import javax.mail.Transport;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeMessage;

/**
 * This sample code is from http://d.hatena.ne.jp/ttshrk/20110517/1305641955. 
 * Depends on https://code.google.com/p/javamail-android/.
 */
public class SendingMailTest
{
    public static void main(String[] args) throws MessagingException
    {
        Properties props = new Properties();
        props.put("mail.smtp.host", "smtp.gmail.com");
        props.put("mail.host", "smtp.gmail.com");
        props.put("mail.smtp.port", "587");
        props.put("mail.smtp.auth", "true");
        props.put("mail.smtp.starttls.enable", "true");

        Session session = Session.getDefaultInstance(props);
        session.setDebug(true);

        MimeMessage msg = new MimeMessage(session);
        msg.setSubject("件名", "utf-8");
        msg.setFrom(new InternetAddress("your_account@gmail.com"));
        msg.setSender(new InternetAddress("your_account@gmail.com"));
        msg.setRecipient(Message.RecipientType.TO, new InternetAddress("to_account@gmail.com"));
        msg.setText("本文", "utf-8");

        Transport t = session.getTransport("smtp");
        t.connect("Gmail Account - something@gmail.com", "password");
        t.sendMessage(msg, msg.getAllRecipients());
    }
}
