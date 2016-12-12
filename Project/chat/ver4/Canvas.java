package com.example.user.chat_oss;

import android.app.Activity;
import android.graphics.Color;
import android.graphics.Rect;
import android.os.Bundle;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.LinearLayout;

/**
 * Created by KH-JIN on 2016. 12. 12..
 */

public class Canvas extends Activity {
    //그리기 뷰 전역 변수.
    private DrawLine drawLine = null;

    @Override
    public void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_canvas);
        /*
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FORCE_NOT_FULLSCREEN,
                WindowManager.LayoutParams.FLAG_FORCE_NOT_FULLSCREEN);*/
    }

    @Override
    public void onWindowFocusChanged(boolean hasFocus)
    {
        //hasFocus : 앱이 화면에 보여졌을때 true로 설정되어 호출됨.
        //만약 그리기 뷰 전역변수에 값이 없을경우 전역변수를 초기화 시킴.
        if(hasFocus && drawLine == null)
        {
            //그리기 뷰가 보여질(나타날) 레이아웃 찾기..
            LinearLayout llCanvas = (LinearLayout)findViewById(R.id.llCanvas);
            if(llCanvas != null) //그리기 뷰가 보여질 레이아웃이 있으면...
            {
                //그리기 뷰 레이아웃의 넓이와 높이를 찾아서 Rect 변수 생성.
                Rect rect = new Rect(0, 0,
                        llCanvas.getMeasuredWidth(), llCanvas.getMeasuredHeight());

                //그리기 뷰 초기화..
                drawLine = new DrawLine(this, rect);

                //그리기 뷰를 그리기 뷰 레이아웃에 넣기 -- 이렇게 하면 그리기 뷰가 화면에 보여지게 됨.
                llCanvas.addView(drawLine);
            }

            //이건.. 상단 메뉴(RED, BLUE ~~~)버튼 설정...
            //일단 초기값은 0번(RED)으로.. ^^
            resetCurrentMode(0);
        }

        super.onWindowFocusChanged(hasFocus);
    }

    //코딩 하기 쉽게 하기 위해서.. 사용할 상단 메뉴 버튼들의 아이디를 배열에 넣는다..
    private int[] btns = {R.id.btnRED, R.id.btnBLUE, R.id.btnGREEN, R.id.btnBLACK, R.id.btnWHITE};
    //코딩 하기 쉽게 하기 위해서.. 상단 메뉴 버튼의 배열과 똑같이 실제 색상값을 배열로 만든다.
    private int[] colors = {Color.RED, Color.BLUE, Color.GREEN, Color.BLACK, Color.WHITE};

    //선택한 색상에 맞도록 버튼의 배경색과 글자색을 바꾸고, 그리기 뷰에도 알려 준다.
    private void resetCurrentMode(int curMode)
    {
        for(int i=0;i<btns.length;i++)
        {
            //이건.. 배열 뒤지면서... 버튼이 있는지 체크..
            Button btn = (Button)findViewById(btns[i]);
            if(btn != null)
            {
                //버튼 있으면 배경색과 글자색 변경..
                //만약 선택한 버튼값과 찾은 버튼이 동일하면 회색배경에 흰색글자 버튼으로 변경.
                //동일하지 않으면 흰색배경에 회색글자 버튼으로 변경.
                btn.setBackgroundColor(i==curMode?0xff555555:0xffffffff);
                btn.setTextColor(i==curMode?0xffffffff:0xff555555);
            }
        }

        //만약 그리기 뷰가 초기화 되었으면, 그리기 뷰에 글자색을 알려줌..
        if(drawLine != null) drawLine.setLineColor(colors[curMode]);
    }

    //버튼을 클릭했을때 호출 되는 함수.
    //이 함수가 호출될때 어떤 버튼(뷰)에서 호출했는지를 같이 알려준다.
    //버튼 클릭시 이 함수를 호출 하게 하기 위해서는...
    //main.xml에서
    //<Button ~~~~ android:onClick="btnClick" ~~~~ />
    //이렇게 btnClick이라는 함수명을 넣어 줘야함.
    public void btnClick(View view)
    {
        if(view == null) return;

        for(int i=0;i<btns.length;i++)
        {
            //배열 뒤지면서 클릭한 버튼이 있는지 확인..
            if(btns[i] == view.getId())
            {
                //만약 선택한 버튼이 있으면.. 버튼모양 및 그리기 뷰 설정을 하기 위해서 함수 호출..
                resetCurrentMode(i);

                //더이상 처리를 할 필요가 없으니까.. for문을 빠져 나옴..
                break;
            }
        }
    }
}
