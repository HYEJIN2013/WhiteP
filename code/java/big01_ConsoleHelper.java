package com.javarush.test.level30.lesson15.big01;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

/**
 * Created by user-pc on 20.05.2016.
 */
public class ConsoleHelper {
    private static BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));

    public static void main(String[] args) {
        System.out.println(readInt());
    }

    public static void writeMessage(String message) {
        System.out.println(message);
    }

    public static String readString() {
        String result;
        try {
            result = reader.readLine();
        } catch (IOException e) {
            System.out.println("Произошла ошибка при попытке ввода текста. Попробуйте еще раз.");
            result = readString();
        }
        return result;
    }

    public static int readInt(){
        int result;
        try {
            result=  Integer.parseInt(readString());
        } catch (NumberFormatException e) {
            System.out.println("Произошла ошибка при попытке ввода числа. Попробуйте еще раз.");
            result = readInt();
        }
        return result;
    }

}
