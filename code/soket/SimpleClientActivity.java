/*
 * This is a simple Android mobile client
 * This application send any file to a remort server when the 
 * send button is pressed
 * Author by Lak J Comspace
 */

package lakj.comspace.simpleclient;

import java.io.BufferedInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.net.Socket;
import java.net.UnknownHostException;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

public class SimpleClientActivity extends Activity {

    private Socket client;
    private FileInputStream fileInputStream;
    private BufferedInputStream bufferedInputStream;
    private OutputStream outputStream;
    private Button button;
    private TextView text;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);

        button = (Button) findViewById(R.id.button1);   //reference to the send button
        text = (TextView) findViewById(R.id.textView1);   //reference to the text view

        //Button press event listener
        button.setOnClickListener(new View.OnClickListener() {

            public void onClick(View v) {

                File file = new File("/mnt/sdcard/input.jpg"); //create file instance

                try {

                    client = new Socket("10.0.2.2", 4444);

                    byte[] mybytearray = new byte[(int) file.length()]; //create a byte array to file

                    fileInputStream = new FileInputStream(file);
                    bufferedInputStream = new BufferedInputStream(fileInputStream);

                    bufferedInputStream.read(mybytearray, 0, mybytearray.length); //read the file

                    outputStream = client.getOutputStream();

                    outputStream.write(mybytearray, 0, mybytearray.length); //write file to the output stream byte by byte
                    outputStream.flush();
                    bufferedInputStream.close();
                    outputStream.close();
                    client.close();

                    text.setText("File Sent");


                } catch (UnknownHostException e) {
                    e.printStackTrace();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        });

    }
}