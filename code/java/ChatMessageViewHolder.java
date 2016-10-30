package com.google.firebase.zerotoapp;

import android.app.Activity;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import com.bumptech.glide.Glide;

public class ChatMessageViewHolder extends RecyclerView.ViewHolder {
    private static final String TAG = "ChatMessageViewHolder";
    private final Activity activity;

    TextView name, message;
    ImageView image;

    public ChatMessageViewHolder(Activity activity, View itemView) {
        super(itemView);
        this.activity = activity;
        name = (TextView) itemView.findViewById(android.R.id.text1);
        message = (TextView) itemView.findViewById(android.R.id.text2);
        image= new ImageView(activity);
        ((ViewGroup)itemView).addView(image);

    }

    public void bind(ChatMessage chat) {
        name.setText(chat.name);
        if (chat.message.startsWith("https://firebasestorage.googleapis.com/") || chat.message.startsWith("content://")) {
            message.setVisibility(View.INVISIBLE);
            image.setVisibility(View.VISIBLE);
            Glide.with(activity)
                    .load(chat.message)
                    .into(image);
        }
        else {
            message.setVisibility(View.VISIBLE);
            image.setVisibility(View.GONE);
            message.setText(chat.message);
        }
    }
}
