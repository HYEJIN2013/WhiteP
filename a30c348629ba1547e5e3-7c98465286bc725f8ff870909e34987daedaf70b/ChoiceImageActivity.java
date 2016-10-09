package me.passos.android.example.choiceimage;

import android.app.Activity;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import static android.provider.MediaStore.Images.Media.*;

public class ChoiceImageActivity extends Activity {

    private int requestCode = 1;
    private ImageView image;
    private TextView url;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);


        image = (ImageView) findViewById(R.id.image);
        url = (TextView) findViewById(R.id.url);

        Button button = (Button) findViewById(R.id.button);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(Intent.ACTION_PICK, EXTERNAL_CONTENT_URI);
                // If you want to crop the image that will be displayed
//                intent.putExtra("crop", "true");
                startActivityForResult(intent, requestCode);
            }
        });
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        if(requestCode == this.requestCode) {
            Uri selectedImage = data.getData();
            image.setImageURI(selectedImage);
            url.setText(selectedImage.toString());
        }
    }
}
