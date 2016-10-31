import javax.microedition.midlet.*;
import javax.microedition.lcdui.*;
import java.util.Timer;
import java.util.TimerTask;

public class SimpleStopWatch extends MIDlet implements CommandListener
{
	Display dsp;
	Form form;
	TextField txt;
	Command start;
	Command pause;
	Command exit;
	Timer timer;
	StartTime st;
	
	public void startApp()
	{
		dsp = Display.getDisplay(this);
		form = new Form("Simple StopWatch");
		txt = new TextField("Waktu","",45, TextField.ANY);
		start = new Command("Start", Command.OK,0);
		pause = new Command("Pause", Command.OK,0);
		exit = new Command("Exit", Command.EXIT,1);
		
		form.append(txt);
		form.addCommand(start);
		form.addCommand(exit);
		form.setCommandListener((CommandListener) this);
		dsp.setCurrent(form);
		
	}
	
	public void pauseApp()
	{
		
	}
	
	public void destroyApp(boolean unconditional)
	{
		
	}
	
	public void commandAction(Command com, Displayable dis)
		{
			if(com == start)
			{
				form.removeCommand(start);
				form.addCommand(pause);
				timer = new Timer();
				st = new StartTime();
				timer.schedule(st,0,100);
			}
			else if(com == pause)
			{
				form.removeCommand(pause);
				form.addCommand(start);
				timer.cancel();
			}
			else if(com == exit)
			{
				destroyApp(false);
				notifyDestroyed();
			}
		}
	public class StartTime extends TimerTask
	{
		int a;
		int dtk, detik, menit, jam;
		public final void run()
		{
			++dtk;
			if(dtk >= 9)
			{
				detik = detik + 1;
				dtk = 0;
			}
			else if(detik > 59)
			{
				menit = menit + 1;
				detik = 0;
			}
			else if(menit > 59)
			{
				jam = jam + 1;
				menit = 0;
			}
			txt.setString(jam + ":" + menit + ":" + detik + ":" + dtk);
		}
	}
}


