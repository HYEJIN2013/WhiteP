package com.example.user.chat_oss;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

public class Image extends AppCompatActivity implements View.OnClickListener {

    private Button btnUpload, btnDownload, btnCaputure, btnCanvas;




    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_image);

        btnUpload = (Button)findViewById(R.id.image_btn_upload);
        btnDownload = (Button)findViewById(R.id.image_btn_download);
        btnCaputure = (Button)findViewById(R.id.image_btn_capture);
        btnCanvas = (Button)findViewById(R.id.image_btn_Canvas);

        btnUpload.setOnClickListener(this);
        btnDownload.setOnClickListener(this);
        btnCaputure.setOnClickListener(this);
        btnCanvas.setOnClickListener(this);
    }

    @Override
    public void onClick(View view) {
        if(view.getId() == R.id.image_btn_upload)
        {
            Intent intent =new Intent(getApplicationContext(),FileUpload.class);
            startActivity(intent);
        }
        else if(view.getId() == R.id.image_btn_capture)
        {
            Intent intent =new Intent(getApplicationContext(),CaptureImage.class);
            startActivity(intent);
        }
        else if(view.getId() == R.id.image_btn_Canvas)
        {
            Intent intent = new Intent(Image.this, Canvas.class);
            startActivity(intent);
        }
    }
}
