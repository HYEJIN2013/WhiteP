/*
Copyright (c) 2015, Gheorghita Stanciu gheorghita(dot)stanciu(at)gmail(dot)com
All rights reserved.
 
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met: 
 
1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer. 
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution. 
 
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 
The views and conclusions contained in the software and documentation are those
of the authors and should not be interpreted as representing official policies, 
either expressed or implied, of the FreeBSD Project.
*/

package com.csr.utils;

import java.io.File;

import java.nio.file.Path;

import java.nio.file.Paths;

import java.util.Date;
import java.util.Iterator;
import java.util.List;
import java.util.Properties;

import javax.activation.DataHandler;
import javax.activation.DataSource;

import javax.activation.FileDataSource;

import javax.mail.Authenticator;
import javax.mail.BodyPart;
import javax.mail.Message;
import javax.mail.Multipart;
import javax.mail.PasswordAuthentication;
import javax.mail.Session;
import javax.mail.Transport;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeBodyPart;
import javax.mail.internet.MimeMessage;
import javax.mail.internet.MimeMultipart;

public class EmailMessage {
    
    public EmailMessage() {
        super();
    }
    
    public void send(String emlFrom, String emlTo, String emlCC, String emlServer,
                     int emlPort, boolean useSSL, String eml_user, String eml_pass,
                     String subiect, String corp_mesaj,
                     List<String> attachements) throws Exception {
        
        if (emlServer.length() == 0
            || emlFrom.length() == 0
            || emlTo.length() == 0
            || emlPort <= 0) {
            throw new Exception("Setarile SMTP nu a fost efectuate corect.");
        }
        
        boolean smtpRequiresLogin = eml_user != null && !eml_user.isEmpty();
        
        Properties props = new Properties();
        props.put("mail.smtp.host", emlServer);
        props.put("mail.smtp.port", String.valueOf(emlPort));
        props.put("mail.smtp.auth", smtpRequiresLogin ? "true" : "false");
        props.put("mail.smtp.starttls.enable", useSSL ? "true" : "false");
        
        Authenticator auth = null;
                
        if (smtpRequiresLogin) {
                auth = new Authenticator() {
                    //override the getPasswordAuthentication method
                    protected PasswordAuthentication getPasswordAuthentication() {
                        return new PasswordAuthentication(eml_user, eml_pass);
                    }
                };
        }
        
        Session session = Session.getInstance(props, auth);
                
        MimeMessage msg = new MimeMessage(session);
                
        msg.addHeader("Content-type", "text/HTML; charset=UTF-8");
        msg.addHeader("format", "flowed");
        msg.addHeader("Content-Transfer-Encoding", "8bit");
        
        msg.setFrom(new InternetAddress(emlFrom, emlFrom));
        msg.setReplyTo(InternetAddress.parse(emlTo, false));
        
        if (emlCC.length() > 0)
            msg.setRecipients(Message.RecipientType.CC, InternetAddress.parse(emlCC, false));
        
        msg.setSubject(subiect, "UTF-8");
        
        msg.setSentDate(new Date());
        
        msg.setRecipients(Message.RecipientType.TO, InternetAddress.parse(emlTo, false));
        
        // Create the message body part
        BodyPart messageBodyPart = new MimeBodyPart();

        // Fill the message
        messageBodyPart.setText(corp_mesaj);
         
        // Create a multipart message for attachment
        Multipart multipart = new MimeMultipart();

        // Set text message part
        multipart.addBodyPart(messageBodyPart);
        
        if (attachements != null) {
            Iterator<String> fileIter = attachements.iterator();
            
            while (fileIter.hasNext()) {
                String file = fileIter.next();
                // next part is attachment
                File testFile = new File(file);
                
                if (testFile.exists()) {
                    Path p = Paths.get(file);
                    String filename = p.getFileName().toString();
                    
                    messageBodyPart = new MimeBodyPart();
                    DataSource source = new FileDataSource(file);
                    messageBodyPart.setDataHandler(new DataHandler(source));
                    messageBodyPart.setFileName(filename);
                    
                    // Set attach message part
                    multipart.addBodyPart(messageBodyPart);
                } else {
                    throw new Exception("File " + file + " was not found.");
                }
            }
        }
    
        // Send the complete message parts
        msg.setContent(multipart);
        
        Transport.send(msg);
    }
}
