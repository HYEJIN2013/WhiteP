// StopWatch
// Simple multiple-stopwatch application
// Author: Christopher Vo (cvo1@cs.gmu.edu)

public class StopWatch extends javax.swing.JFrame {
  private static final long serialVersionUID = -7040646868513878300L;
  private static int numTimers = 5;

  public StopWatch() {
    // make main window
    setTitle("Timers");
    setLayout(new java.awt.GridLayout(numTimers, 1));
    setDefaultCloseOperation(javax.swing.JFrame.EXIT_ON_CLOSE);
    setResizable(false);

    // add stopwatch panels
    for (int i = 0; i < numTimers; i++)
      add(new StopWatchPanel(this));

    // show the main window
    pack();
    setLocationRelativeTo(null);
    setVisible(true);
    repaint();
  }

  public static void main(String args[]) {
    new StopWatch();
  }
}