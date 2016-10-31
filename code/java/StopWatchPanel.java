// StopWatchPanel
// Simple multiple-stopwatch application (Panel)
// Author: Christopher Vo (cvo1@cs.gmu.edu)

import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.util.regex.*;
import javax.sound.sampled.*;
import javax.swing.*;

public class StopWatchPanel extends JPanel implements ActionListener, Runnable {
  private static final long serialVersionUID = 1220584852629632807L;
  private static final Insets stdInset = new Insets(5, 5, 5, 5);
  private JTextField name, time;
  private JButton startStopButton, resetButton;
  private long setTime, lapTime, startTime, timeLeft;
  private Boolean running = false;
  private static final String SOUND_PIKACHU = "pikachu.wav";
  private Thread timerThread;
  private Clip currentClip;
  private final Runnable displayUpdater = new Runnable() {
    public void run() {
      time.setText(millisToStr(timeLeft));
    }
  };

  private void saveTime() {
    time.getCaret().setVisible(false);
    time.setEditable(false);
    setTime = strToMillis(time.getText());
    lapTime = setTime;
    time.setText(millisToStr(setTime));
  }

  public StopWatchPanel(final JFrame parentFrame) {

    // name field ------------------------------------------
    name = new JTextField("Event");
    name.setMargin(stdInset);
    name.setEditable(false);
    // double click: edit
    name.addMouseListener(new MouseAdapter() {
      public void mouseClicked(MouseEvent e) {
        if (e.getClickCount() >= 2)
          name.setEditable(true);
      }
    });
    // focus lost: save
    name.addFocusListener(new FocusAdapter() {
      public void focusLost(FocusEvent e) {
        name.setEditable(false);
        parentFrame.pack();
      }
    });
    // enter: save
    name.addKeyListener(new KeyAdapter() {
      public void keyPressed(KeyEvent e) {
        if (e.getKeyCode() == KeyEvent.VK_ENTER) {
          name.setEditable(false);
          parentFrame.pack();
        }
      }
    });

    // time field ------------------------------------------
    time = new JTextField("00:00:00.000");
    time.setFont(new Font(Font.MONOSPACED, Font.PLAIN, 12));
    time.setMargin(stdInset);
    time.setEditable(false);
    // double click: stop timer and edit
    time.addMouseListener(new MouseAdapter() {
      public void mouseClicked(MouseEvent e) {
        if (e.getClickCount() == 2) {
          stopTimer();
          time.setEditable(true);
          time.getCaret().setVisible(true);
        }
      }
    });
    // focus lost: save
    time.addFocusListener(new FocusAdapter() {
      public void focusLost(FocusEvent e) {
        saveTime();
        parentFrame.pack();
      }
    });
    // enter: save
    time.addKeyListener(new KeyAdapter() {
      public void keyPressed(KeyEvent e) {
        if (e.getKeyCode() == KeyEvent.VK_ENTER) {
          saveTime();
          parentFrame.pack();
        }
      }
    });

    // buttons ------------------------------------------
    resetButton = new JButton("Reset");
    resetButton.addActionListener(new ActionListener() {
      public void actionPerformed(ActionEvent e) {
        stopTimer();
        startTime = lapTime = setTime;
        time.setText(millisToStr(setTime));
        if (currentClip != null && currentClip.isRunning()) {
          currentClip.stop();
          currentClip.close();
          currentClip = null;
        }
      }
    });
    startStopButton = new JButton("Start / Stop");
    startStopButton.addActionListener(this);

    // widget layout ------------------------------------------
    setLayout(new FlowLayout(FlowLayout.RIGHT, 5, 5));
    add(name);
    add(time);
    add(resetButton);
    add(startStopButton);
  }

  // convert string from 00:00:00.000 to milliseconds
  public static long strToMillis(String time) {
    long result = 0;
    try {
      Pattern p = Pattern
          .compile("([0-9]{1,2}):([0-9]{1,2}):([0-9]{1,2})(\\.([0-9]{1,3}))?");
      Matcher m = p.matcher(time.trim());
      m.find();
      result += Long.parseLong(m.group(1)) * 3600000
          + Long.parseLong(m.group(2)) * 60000 + Long.parseLong(m.group(3))
          * 1000;
      if (m.group(5) != null)
        result += Long.parseLong(m.group(5));
    } catch (Exception e) {
      // don't complain, just return 0
      return 0;
    }
    return result;
  }

  // convert milliseconds to 00:00:00.000
  public static String millisToStr(long time) {
    long ms = time;
    long h = ms / 3600000;
    ms = ms % 3600000;
    long m = ms / 60000;
    ms = ms % 60000;
    long s = ms / 1000;
    ms = ms % 1000;
    return String.format("%02d:%02d:%02d.%03d", h, m, s, ms);
  }

  // start stop button action
  public void actionPerformed(ActionEvent e) {
    if (time.isEditable())
      return;
    if (running) {
      running = false;
      try {
        timerThread.join();
      } catch (InterruptedException ie) {
      }
      lapTime = timeLeft;
      time.setText(millisToStr(timeLeft));
    } else {
      startTime = System.currentTimeMillis();
      running = true;
      timerThread = new Thread(this);
      timerThread.start();
    }
  }

  // stop the timer and clean up the thread.
  public void stopTimer() {
    running = false;
    try {
      if (timerThread != null && timerThread.isAlive()) {
        timerThread.join();
      }
    } catch (Exception ie) {
    }
  }

  // play a given sound file.
  private void playSound(String sound) {
    try {
      BufferedInputStream soundFileStream = new BufferedInputStream(this
          .getClass().getResourceAsStream(sound));
      AudioInputStream audioInputStream = AudioSystem
          .getAudioInputStream(soundFileStream);
      AudioFormat audioFormat = audioInputStream.getFormat();
      DataLine.Info dataLineInfo = new DataLine.Info(Clip.class, audioFormat);
      if (currentClip != null && currentClip.isRunning()) {
        currentClip.stop();
        currentClip.close();
        currentClip = null;
      }
      currentClip = (Clip) AudioSystem.getLine(dataLineInfo);
      currentClip.open(audioInputStream);
      currentClip.start();
    } catch (Exception e) {
      e.printStackTrace();
    }
  }

  @Override
  public void run() {
    try {
      while (running) {
        timeLeft = lapTime - (System.currentTimeMillis() - startTime);
        if (timeLeft <= 0) {
          playSound(SOUND_PIKACHU);
          timeLeft = 0;
          lapTime = 0;
          running = false;
        }
        SwingUtilities.invokeAndWait(displayUpdater);
        Thread.sleep(50);
      }
    } catch (Exception e) {
    }
  }
}