package com.example.user.chat_oss;

import android.content.Context;
import android.graphics.*;
import android.view.MotionEvent;
import android.view.View;

/**
 * Created by KH-JIN on 2016. 12. 12..
 */

public class DrawLine extends View {
    //현재 그리기 조건(색상, 굵기, 등등.)을 기억 하는 변수.
    private Paint paint = null;

    //그리기를 할 bitmap 객체. -- 도화지라고 생각하면됨.
    private Bitmap bitmap = null;

    //bitmap 객체의 canvas 객체. 실제로 그리기를 하기 위한 객체.. -- 붓이라고 생각하면됨.
    private android.graphics.Canvas canvas = null;

    //마우스 포인터(손가락)이 이동하는 경로 객체.
    private Path path;

    //마우스 포인터(손가락)이 가장 마지막에 위치한 x좌표값 기억용 변수.
    private float   oldX;

    //마우스 포인터(손가락)이 가장 마지막에 위치한 y좌표값 기억용 변수.
    private float   oldY;

    /**
     * 생성자.. new DrawLine(this, rect) 하면 여기가 호출됨.
     * @param context   Context객체
     * @param rect      그리기 범위 화면 사이즈
     */
    public DrawLine(Context context, Rect rect)
    {
        this(context);

        //그리기를 할 bitmap 객체 생성.
        bitmap = Bitmap.createBitmap(rect.width(), rect.height(),
                Bitmap.Config.ARGB_8888);
        //그리기 bitmap에서 canvas를 알아옴.
        canvas = new android.graphics.Canvas(bitmap);

        //경로 초기화.
        path = new Path();
    }

    @Override
    protected void onDetachedFromWindow()
    {
        //앱 종료시 그리기 bitmap 초기화 시킴...
        if(bitmap!= null) bitmap.recycle();
        bitmap = null;

        super.onDetachedFromWindow();
    }

    @Override
    public void onDraw(android.graphics.Canvas canvas)
    {
        //그리기 bitmap이 있으면 현재 화면에 bitmap을 그린다.
        //자바의 view는 onDraw할때 마다 화면을 싹 지우고 다시 그리게 됨.
        if(bitmap != null)
        {
            canvas.drawBitmap(bitmap, 0, 0, null);
        }
    }



    //이벤트 처리용 함수..
    @Override
    public boolean onTouchEvent(MotionEvent event)
    {

        float x = event.getX();
        float y = event.getY();

        switch (event.getAction() & MotionEvent.ACTION_MASK)
        {
            case MotionEvent.ACTION_DOWN:
            {
                //최초 마우스를 눌렀을때(손가락을 댓을때) 경로를 초기화 시킨다.
                path.reset();

                //그다음.. 현재 경로로 경로를 이동 시킨다.
                path.moveTo(x, y);

                //포인터 위치값을 기억한다.
                oldX = x;
                oldY = y;

                //계속 이벤트 처리를 하겠다는 의미.
                return true;
            }
            case MotionEvent.ACTION_MOVE:
            {
                //포인트가 이동될때 마다 두 좌표(이전에눌렀던 좌표와 현재 이동한 좌료)간의 간격을 구한다.
                float dx = Math.abs(x - oldX);
                float dy = Math.abs(y - oldY);

                //두 좌표간의 간격이 4px이상이면 (가로든, 세로든) 그리기 bitmap에 선을 그린다.
                if (dx >= 4 || dy >= 4)
                {
                    //path에 좌표의 이동 상황을 넣는다. 이전 좌표에서 신규 좌표로..
                    //lineTo를 쓸수 있지만.. 좀더 부드럽게 보이기 위해서 quadTo를 사용함.
                    path.quadTo(oldX, oldY, x, y);


                    //포인터의 마지막 위치값을 기억한다.
                    oldX = x;
                    oldY = y;

                    //그리기 bitmap에 path를 따라서 선을 그린다.
                    canvas.drawPath(path, paint);
                }

                //화면을 갱신시킴.. 이 함수가 호출 되면 onDraw 함수가 실행됨.
                invalidate();

                //계속 이벤트 처리를 하겠다는 의미.
                return true;
            }
        }

        //더이상 이벤트 처리를 하지 않겠다는 의미.
        return false;
    }

    /**
     * 펜 색상 세팅
     * @param color 색상
     */
    public void setLineColor(int color)
    {
        paint = new Paint();
        paint.setColor(color);

        paint.setAlpha(255);
        paint.setDither(true);
        paint.setStrokeWidth(10);
        paint.setStrokeJoin(Paint.Join.ROUND);
        paint.setStyle(Paint.Style.STROKE);
        paint.setStrokeCap(Paint.Cap.ROUND);
        paint.setAntiAlias(true);
    }


    public DrawLine(Context context)
    {
        super(context);
    }
}
