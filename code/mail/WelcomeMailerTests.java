package com.example.mail;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

import java.io.InputStreamReader;
import java.io.Reader;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

import javax.inject.Inject;
import javax.mail.Message;
import javax.mail.NoSuchProviderException;
import javax.mail.Session;
import javax.mail.Transport;
import javax.mail.internet.MimeMessage;

import org.junit.Before;
import org.junit.Test;
import org.jvnet.mock_javamail.Mailbox;
import org.springframework.core.io.FileSystemResourceLoader;
import org.springframework.core.io.ResourceLoader;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.JavaMailSenderImpl;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.mail.javamail.MimeMessagePreparator;
import org.springframework.scheduling.annotation.Async;

// little example of email sending with spring java mail & jmustache templating; uses mock javamail API for unit testing.
// relies on Mock JavaMail library in the classpath: testCompile 'org.jvnet.mock-javamail:mock-javamail:1.9'
public class WelcomeMailerTests {

    private WelcomeMailer mailer;

    @Before
    public void setUp() {
        JavaMailSenderImpl mailSender = new JavaMailSenderImpl();
        JMustacheStringTemplateLoader templateLoader = new JMustacheStringTemplateLoader(new FileSystemResourceLoader());
        templateLoader.setPrefix("src/main/webapp/WEB-INF/views/"); // where our templates are located
        mailer = new WelcomeMailer(mailSender, templateLoader);
    }
    
    @Test
    public void sendMail() throws Exception {
        Subscriber subscriber = new Subscriber("keith.donald@gmail.com", new Name("Keith", "Donald"));
        mailer.mail(subscriber);
        // assert the message was delivered with the correct content
        assertEquals(1, Mailbox.get("keith.donald@gmail.com").getNewMessageCount());
        Message message = Mailbox.get("keith.donald@gmail.com").get(0);
        assertEquals("Welcome Keith", message.getSubject());
        assertTrue(((String) message.getContent()).contains("keith.donald@gmail.com"));        
    }

    public class WelcomeMailer {

        private JavaMailSender mailSender;

        private StringTemplateLoader templateLoader;
        
        @Inject
        public WelcomeMailer(JavaMailSender mailSender, StringTemplateLoader templateLoader) {
            this.mailSender = mailSender;
            this.templateLoader = templateLoader;
        }
        
        @Async // <-- to work needs AOP either via JDK proxies, cglib, or AspectJ
        public void mail(final Subscriber subscriber) {
            MimeMessagePreparator preparator = new MimeMessagePreparator() {
                public void prepare(MimeMessage message) throws Exception {
                   MimeMessageHelper welcome = new MimeMessageHelper(message);
                   welcome.setFrom("My App <info@example.com>");
                   welcome.setTo(subscriber.getEmail());
                   welcome.setSubject("Welcome " + subscriber.getName().getFirstName());
                   Map<String, Object> model = new HashMap<String, Object>();
                   model.put("firstName", subscriber.getName().getFirstName());
                   model.put("body", welcomeBody(subscriber));
                   welcome.setText(templateLoader.getTemplate("mail/letter").render(model), true);
                }
             };        
            mailSender.send(preparator);
        }

        private String welcomeBody(Subscriber subscriber) {
            Map<String, Object> model = new HashMap<String, Object>(); 
            model.put("email", subscriber.getEmail());
            return templateLoader.getTemplate("mail/welcome-body").render(model);
        }
        
        // ugly cglib ceremony
        public WelcomeMailer() {};

    }
    
    // little string template abstraction so we don't depend so heavily on jmustache api
    
    public interface StringTemplateLoader {
        
        StringTemplate getTemplate(String location);
        
    }
    
    public interface StringTemplate {

        String render(Map<String, Object> model);

    }
    
    // relies on JMustache: compile 'com.samskivert:jmustache:1.5'
    public static class JMustacheStringTemplateLoader implements StringTemplateLoader {

        private final com.samskivert.mustache.Mustache.TemplateLoader templateLoader;

        private final com.samskivert.mustache.Mustache.Compiler compiler;

        private String prefix = "/WEB-INF/views/";
        
        private String suffix = ".html";
        
        public JMustacheStringTemplateLoader(ResourceLoader resourceLoader) {
            templateLoader = new ResourceTemplateLoader(resourceLoader);
            compiler = com.samskivert.mustache.Mustache.compiler().nullValue("").escapeHTML(false).withLoader(templateLoader);
        }

        public void setPrefix(String prefix) {
            this.prefix = prefix;
        }
        
        public void setSuffix(String suffix) {
            this.suffix = suffix;
        }
        
        public StringTemplate getTemplate(String location) {
            Reader source = null;
            try {
               source = templateLoader.getTemplate(prefix + location + suffix);
            } catch (Exception e) {
                throw new RuntimeException(e);
            }
            com.samskivert.mustache.Template template = compiler.compile(source);
            return new JMustacheStringTemplate(template);        
        }

        private static class ResourceTemplateLoader implements com.samskivert.mustache.Mustache.TemplateLoader {

            private static final String DEFAULT_ENCODING = "UTF-8";

            private final ResourceLoader resourceLoader;

            private String encoding = DEFAULT_ENCODING;

            public ResourceTemplateLoader(ResourceLoader resourceLoader) {
                this.resourceLoader = resourceLoader;
            }

            @Override
            public Reader getTemplate(String name) throws Exception {
                return new InputStreamReader(resourceLoader.getResource(name).getInputStream(), encoding);
            }

        }
        
        private static class JMustacheStringTemplate implements StringTemplate {

            private com.samskivert.mustache.Template template;
            
            public JMustacheStringTemplate(com.samskivert.mustache.Template template) {
                this.template = template;
            }

            public String render(Map<String, Object> model) {
                return template.execute(model);
            }
            
        }

    }
    
    // example html email templates adapted from mailchimp and mint.com
    
    /* src/main/webapp/WEB-INF/views/mail/letter.html
    *
    * <!DOCTYPE html>
    <html>
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title></title>
    </head>
    <body style="margin: 0; padding: 0; background-color: #color;" leftmargin="0" marginheight="0" marginwidth="0" topmargin="0" leftmargin="0">
        <table border="0" cellpadding="0" cellspacing="0" width="100%">
            <tr>
                <td bgcolor="e6fdc4" style="background-color: ##color">
                    <table border="0" cellpadding="0" cellspacing="0" width="600" align="center">
                        <tr>
                            <td height="15" />
                        </tr>
                        <tr>
                            <td bgcolor="white" style="border-radius: 10px; -moz-border-radius: 10px; -webkit-border-radius: 10px; -khtml-border-radius: 10px; -webkit-box-shadow: 0px 0px 10px r=gba(0, 0, 0, 0.2); -moz-box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);">
                                <!-- Header -->
                                <table border="0" cellpadding="15" cellspacing="0" width="100%">
                                    <tr>
                                        <td align="center"><img src="http://url/static/images/logo.png" style="max-width: 600px;" /></td>
                                    </tr>
                                </table>
                                <!-- Body -->
                                <table border="0" cellpadding="15" cellspacing="0" width="100%">
                                    <tr>
                                        <td>
                                            <div style="font-family: Helvetica, Arial, sans-serif; font-size: 13px; line-height: 150%; margin-top: 0; margin-bottom: 0; padding: 0; color: #color;">
                                                {{firstName}},<br />
                                                <br />
                                                {{body}}<br />
                                                <br />
                                                Sincerely,<br />
                                                <br />
                                                Me
                                            </div>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                        <tr>
                            <td height="15" />
                        </tr>
                    </table>
                </td>
        </table>
    </body>
    </html>
     */
        
    /* src/main/webapp/WEB-INF/views/mail/welcome-body.html
     * 
     * Congratulations, you subscribed as {{email}}, blah blah... <br/>
     */

}