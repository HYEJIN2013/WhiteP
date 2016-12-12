package com.example.user.chat_oss;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;

/**
 * Created by KH-JIN on 2016. 12. 12..
 */

public class First extends AppCompatActivity implements View.OnClickListener {

    Button btn_first;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_first);

        btn_first = (Button)findViewById(R.id.btn_first);
    }

    @Override
    public void onClick(View view) {
        if (view.getId() == R.id.btn_first)
        {
            Intent intent = new Intent(First.this, LogIn.class);
            startActivity(intent);
        }
    }
}
