package tiy.networking;

import java.text.DecimalFormat;
import java.time.Instant;

/**
 * Created by Corey Shaw on 4/27/2016.
 */
public class ThreadRunner {
    public static void main(String[] args) {
        System.out.println("ThreadRunner running");

        int numThreadsStarted = 0;
        DecimalFormat timerFormatter = new DecimalFormat("###,###");

        long startMillis = Instant.now().toEpochMilli();

        while (true) {
            System.out.println("Number of threads started = " + numThreadsStarted);
            SampleThread localThread = new SampleThread();
            Thread newThread = new Thread(localThread);
           //localThread.run();
            newThread.start();
            numThreadsStarted++;
            if (numThreadsStarted > 10) {
                break;
            }
        }

        long endMillis = Instant.now().toEpochMilli();

        System.out.println("Ran in " + timerFormatter.format(endMillis - startMillis) + " ms");

        System.out.println("ThreadRunner done!");
    }
}

