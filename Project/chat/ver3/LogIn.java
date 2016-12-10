package com.example.user.chat_oss;

import android.content.Intent;
import android.support.annotation.NonNull;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.RelativeLayout;
import android.widget.TextView;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;

public class LogIn extends AppCompatActivity implements View.OnClickListener {

    Button btnLogin;
    EditText input_email,input_password;
    TextView btnSignup,btnForgotPass;

    RelativeLayout activity_main;

    private FirebaseAuth auth;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        //View
        btnLogin = (Button)findViewById(R.id.login_btn_login);
        input_email = (EditText)findViewById(R.id.login_email);
        input_password= (EditText)findViewById(R.id.login_password);
        btnSignup = (TextView)findViewById(R.id.login_btn_singup);
        btnForgotPass = (TextView)findViewById(R.id.login_btn_forgot_password);
        activity_main = (RelativeLayout)findViewById(R.id.activity_main);

        btnSignup.setOnClickListener(this);
        btnForgotPass.setOnClickListener(this);
        btnLogin.setOnClickListener(this);

        //Init firebase Auth
        auth = FirebaseAuth.getInstance();

        //check already session , if OK - > DashBoard
        if(auth.getCurrentUser() != null)
           startActivity(new Intent(LogIn.this,DashBoard.class));
    }

    @Override
    public void onClick(View view) {
        if (view.getId() == R.id.login_btn_forgot_password)
        {
            startActivity(new Intent(LogIn.this, ForgotPassword.class));
            finish();
        }
        else if (view.getId() == R.id.login_btn_singup)
        {
            startActivity(new Intent(LogIn.this, SignUp.class));
            finish();
        }
        else if (view.getId() == R.id.login_btn_login)
        {
            loginUser(input_email.getText().toString(),input_password.getText().toString());
        }
    }

    private void loginUser(String email, final String password)
    {
        auth.signInWithEmailAndPassword(email,password)
                .addOnCompleteListener(this, new OnCompleteListener<AuthResult>() {
                    @Override
                    public void onComplete(@NonNull Task<AuthResult> task)
                    {
                        if(!task.isSuccessful())
                        {
                            if(password.length() < 6)
                            {
                                Snackbar snackBar = Snackbar.make(activity_main,"password length must be over 6",Snackbar.LENGTH_SHORT);
                                snackBar.show();
                            }
                        }
                        else
                        {
                            startActivity(new Intent(LogIn.this,DashBoard.class));
                        }
                    }
                });
    }
}
