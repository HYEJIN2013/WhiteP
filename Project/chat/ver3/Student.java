package com.example.ameerhamza.firebabseyoutubetest;

/**
 * Created by AmeerHamza on 9/18/2016.
 */
public class Student {


    private  String name;
    private String emailId;
    private int age;
    private String myKey;
    private  String imageurl;

    public String getImageurl() {
        return imageurl;
    }

    public String getMyKey() {
        return myKey;
    }

    public Student(String emailId, int age, String name,String imageurl) {
        this.emailId = emailId;
        this.age = age;
        this.name = name;
        this.imageurl=imageurl;
    }

    public Student() {
    }

    public String getName() {
        return name;
    }

    public int getAge() {
        return age;
    }

    public String getEmailId() {
        return emailId;
    }


}
