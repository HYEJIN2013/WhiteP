Enter file contents herepackage com.example.suyeon.fileex2;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.net.Socket;
import java.util.ArrayList;



import android.app.Activity;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Environment;
import android.os.StrictMode;
import android.text.method.ScrollingMovementMethod;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.params.HttpConnectionParams;
import org.apache.http.params.HttpParams;
import org.apache.http.util.EntityUtils;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FilenameFilter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;
import java.util.ArrayList;


public class MainActivity extends Activity {
    String mRoot = ""; //SD 카드 저장 경로
    String mPath = ""; //파일 저장된 위치
    TextView mTextmsg;
    ListView mListFile;
    ArrayList<String> mArFile;
    String strItem = ""; //파일명
    TextView mTextFile;
    String[] fileList;
    Button sendBtn;
    /***********소켓 통신을 위한 변수******************/
    Socket mSock = null;
    String talkmsg = "";
    /************************************************/
    AdapterView.OnItemClickListener mItemClickListener =
            new AdapterView.OnItemClickListener(){
                public void onItemClick(AdapterView parent, View view, int position,
                                        long id){
                    strItem = mArFile.get(position);
                    mTextmsg.setText(strItem);
                    mRoot += strItem;
                    ReadTextAssets(mRoot, "KakaoTalkChats.txt");
                }
            };


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mTextFile = (TextView)this.findViewById(R.id.readFile);
        mTextFile.setVerticalScrollBarEnabled(true);
        mTextFile.setMovementMethod(new ScrollingMovementMethod());

        sendBtn = (Button)findViewById(R.id.sendBtn);
        sendBtn.setOnClickListener(new Button.OnClickListener() {
            public void onClick(View v) {
                //코드작성
                String url = "http://192.168.81.1:9080/KakaoTalkServer/Kakao.jsp";
                HttpClient http = new DefaultHttpClient();
                try {

                    ArrayList<NameValuePair> nameValuePairs =
                            new ArrayList<NameValuePair>();
                    nameValuePairs.add(new BasicNameValuePair("name", "유재석"));

                    HttpParams params = http.getParams();
                    HttpConnectionParams.setConnectionTimeout(params, 5000);
                    HttpConnectionParams.setSoTimeout(params, 5000);

                    HttpPost httpPost = new HttpPost(url);
                    UrlEncodedFormEntity entityRequest =
                            new UrlEncodedFormEntity(nameValuePairs, "EUC-KR");

                    httpPost.setEntity(entityRequest);

                    HttpResponse responsePost = http.execute(httpPost);
                    HttpEntity resEntity = responsePost.getEntity();

                    mTextFile.setText( EntityUtils.toString(resEntity));
                }catch(Exception e){e.printStackTrace();}
            }
        });

        if(isSdCard() == false)
            finish();
        mTextmsg = (TextView)findViewById(R.id.textMessage);
        mRoot = Environment.getExternalStorageDirectory().getAbsolutePath();
        mRoot += "/KakaoTalk/Chats/";
        String[] fileList = getFileList(mRoot);
        for(int i=0;i<fileList.length;i++)
            Log.d("tag", fileList[i]);
        initListView();
        fileList2Array(fileList);
        /*************파일전송***********/
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);
        /************************/
    }


    public boolean isSdCard() {
        String ext = Environment.getExternalStorageState();
        if(ext.equals(Environment.MEDIA_MOUNTED) == false){
            Toast.makeText(this, "SD Card does not exist",
                    Toast.LENGTH_SHORT).show();
            return false;
        }

        return true;
    }

    public String[] getFileList(String strPath){
        File fileRoot = new File(strPath);
        if(fileRoot.isDirectory() == false)
            return null;
        mPath = strPath;
        mTextmsg.setText(mPath);

        //   FilenameFilter filter = new FilenameFilter() {
        //       @Override
        //       public boolean accept(File dir, String filename) {
        //           return filename.endsWith(".txt");
        //       }
        //   };

        //   String[] fileList = fileRoot.list(filter);
        fileList = fileRoot.list();
        return fileList;
    }

    public void initListView(){
        mArFile = new ArrayList<String>();
        ArrayAdapter<String> adapter = new ArrayAdapter<String>(this,
                android.R.layout.simple_list_item_1, mArFile);
        mListFile = (ListView)findViewById(R.id.listFile);
        mListFile.setAdapter(adapter);
        mListFile.setOnItemClickListener(mItemClickListener); //ListView 클릭시
    }

    public void fileList2Array(String[] fileList){
        if( fileList == null)
            return;
        mArFile.clear();

        if(mRoot.length() < mPath.length())
            mArFile.add("..");

        for(int i=0;i<fileList.length;i++){
            Log.d("tag",fileList[i]);
            mArFile.add(fileList[i]);
        }

        ArrayAdapter adapter = (ArrayAdapter)mListFile.getAdapter();
        adapter.notifyDataSetChanged();
    }

    public void ReadTextAssets(String mPath, String strFileName){
        String state= Environment.getExternalStorageState();
        File path;    //저장 데이터가 존재하는 디렉토리경로
        File file;

        if( !(state.equals(Environment.MEDIA_MOUNTED) || state.equals(Environment.MEDIA_MOUNTED_READ_ONLY)) ){

            Toast.makeText(this, "SDcard Not Mounted", Toast.LENGTH_SHORT).show();

            return;

        }

        StringBuffer buffer= new StringBuffer();
        path = new File(mPath);
        //path= Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS);
        //for(int i=0;i<fileList.length;i++){
        //    path += fileList[i];
        // }
        file= new File(path, strFileName);


        try {
            FileReader in= new FileReader(file);
            BufferedReader reader= new BufferedReader(in);
            String str= reader.readLine();
            //Log.d("tag","path==========="+path);
            //Log.d("tag","filename==========="+strFileName);

            while( str!=null ){
                buffer.append(str+"\n");
                str= reader.readLine();//한 줄씩 읽어오기
            }
            mTextFile.setText(buffer.toString());
            reader.close();
        } catch (Exception e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }

    private class ConnectTask extends AsyncTask<String, String, String> {
        protected String doInBackground(String... arg){
            try{
                int nPort = 7777;
                mSock = new Socket(arg[0],nPort);

            }catch (Exception e){
                Log.d("tag","Socket connect error");
                return "Connect Fail";
            }
            return "Connect Succeed";
        }

        protected void onPostExecute(String result){
            mTextmsg.setText(result);
        }
    }

    public void onBtnConnect(){
        if(mSock != null)
            return;
        String serverAddr = ""; //IP 주소
        String strPort = "7777";

        new ConnectTask().execute(serverAddr, strPort);
    }


}
