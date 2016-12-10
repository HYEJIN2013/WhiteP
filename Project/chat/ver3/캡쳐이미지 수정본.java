package com.example.user.chat_oss;

import android.app.ProgressDialog;
import android.content.Intent;
import android.net.Uri;
import android.provider.MediaStore;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Toast;

import com.google.android.gms.tasks.OnSuccessListener;
import com.google.firebase.storage.FirebaseStorage;
import com.google.firebase.storage.StorageReference;
import com.google.firebase.storage.UploadTask;
import com.squareup.picasso.Picasso;

public class CaptureImage extends AppCompatActivity {

    private Button mUploadBtn;
    private ImageView mImageView;
    private Uri filepath;

    private static final int CAMERA_REQUEST_CODE = 1;

    private StorageReference mStorage;
    private ProgressDialog mProgress;



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_capture_image);

        mStorage = FirebaseStorage.getInstance().getReference();

        mUploadBtn = (Button)findViewById(R.id.upload);
        mImageView = (ImageView)findViewById(R.id.capture);

        mProgress = new ProgressDialog(this);

        mUploadBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                Intent intent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);

                startActivityForResult(intent, CAMERA_REQUEST_CODE);

            }
        });
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if(requestCode==CAMERA_REQUEST_CODE && resultCode==RESULT_OK){



            mProgress.setMessage("Uploading Image...");
            mProgress.show();

            Uri uri = data.getData();

            StorageReference filepath = mStorage.child("photos").child(uri.getLastPathSegment());

            filepath.putFile(uri).addOnSuccessListener(new OnSuccessListener<UploadTask.TaskSnapshot>() {
                @Override
                public void onSuccess(UploadTask.TaskSnapshot taskSnapshot) {

                    mProgress.dismiss();

                    Uri downloadUri = taskSnapshot.getDownloadUrl();

                    Picasso.with(CaptureImage.this).load(downloadUri).fit().centerCrop().into(mImageView);

                    Toast.makeText(CaptureImage.this, "Uploading finished...", Toast.LENGTH_LONG).show();

                }
            });

        }
    }
}
