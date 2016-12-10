package com.example.user.chat_oss;

import android.content.Intent;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import com.google.firebase.database.ChildEventListener;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

public class ChatRoom extends AppCompatActivity implements View.OnClickListener {

    private Button btn_sen_msg,btn_Image;
    private EditText input_msg;
    private TextView chat_conversation;


    private  String user_name,room_name;
    private DatabaseReference root;
    private String temp_key;


    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_chat_room);

        btn_sen_msg = (Button) findViewById(R.id.btn_send);
        btn_Image = (Button)findViewById(R.id.btn_image);
        input_msg = (EditText) findViewById(R.id.msg_input);
        chat_conversation = (TextView) findViewById(R.id.textView);

        user_name = getIntent().getExtras().get("user_name").toString();
        room_name = getIntent().getExtras().get("room_name").toString();
        setTitle(" Room - "+room_name);

        btn_Image.setOnClickListener(this);

        root = FirebaseDatabase.getInstance().getReference().child(room_name);

        btn_sen_msg.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view) {

                Map<String,Object> map = new HashMap<String, Object>();
                temp_key = root.push().getKey();
                root.updateChildren(map);

                DatabaseReference message_root = root.child(temp_key);
                Map<String,Object> map2 = new HashMap<String, Object>();
                map2.put("name",user_name);
                map2.put("msg",input_msg.getText().toString());

                message_root.updateChildren(map2);


            }
        });
        root.addChildEventListener(new ChildEventListener() {
            @Override
            public void onChildAdded(DataSnapshot dataSnapshot, String s) {

                append_chat_converstion(dataSnapshot);

            }

            @Override
            public void onChildChanged(DataSnapshot dataSnapshot, String s) {

                append_chat_converstion(dataSnapshot);

            }

            @Override
            public void onChildRemoved(DataSnapshot dataSnapshot) {

            }

            @Override
            public void onChildMoved(DataSnapshot dataSnapshot, String s) {

            }

            @Override
            public void onCancelled(DatabaseError databaseError) {

            }
        });
    }
    private  String chat_msg,chat_user_name;

    private void append_chat_converstion(DataSnapshot dataSnapshot) {
        Iterator i = dataSnapshot.getChildren().iterator();
        while(i.hasNext()){

            chat_msg = (String)((DataSnapshot)i.next()).getValue();
            chat_user_name = (String)((DataSnapshot)i.next()).getValue();

            chat_conversation.append(chat_user_name+" : "+chat_msg +"\n");


        }
    }

    @Override
    public void onClick(View view) {
        if(view.getId() == R.id.btn_image)
        {
            Intent intent =new Intent(getApplicationContext(),Image.class);
            startActivity(intent);
        }
    }
}
