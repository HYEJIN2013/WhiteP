package tiy.networking;

import java.text.DecimalFormat;
import java.time.Instant;

/**
 * Created by Tisha868 on 4/27/16.
 */
public class ThreadRunner {

    public static void main(String[] args) {

        System.out.println("ThreadRunner running");

        int numThreadsStarted = 0;
        DecimalFormat timerFormatter = new DecimalFormat("###,###");

        long startMillis = Instant.now().toEpochMilli(); // gets the # of mili seconds, to get # of miliseconds to
        // get # when u start & end.

        while (true) { // as long as i havent started 10 threads stay in loop
            System.out.println("Number of threads started = " + numThreadsStarted);
            SampleThread localThread = new SampleThread(); // cre8 objects of type sample thread

//            Thread newThread = new Thread(localThread); // cre8 new thread, then pass the instance of that class.
//            newThread.start();

            localThread.run();
            numThreadsStarted++;
            if (numThreadsStarted > 10) {
                break;
            }
        }

        long endMillis = Instant.now().toEpochMilli();

        System.out.println("Ran in " + timerFormatter.format(endMillis - startMillis) + " ms");

        System.out.println("ThreadRunner done ^.^ ");
    }
}


