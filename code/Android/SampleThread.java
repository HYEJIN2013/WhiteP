package tiy.networking;

/**
 * Created by Tisha868 on 4/27/16.
 */
public class SampleThread implements Runnable { // have to make it runnable interface has 1 method 1= run that cant
// throw exception.

        public void run() { //run method.
            // y cant run throw exception??
            System.out.println("Running " + Thread.currentThread().getId());

            try {
                Thread.sleep(2000); //Thread.sleep throws exception. All it does is sleep for 2000 miliseconds = 2
                // seconds
            } catch (Exception exception) {
                exception.printStackTrace();
            }

            System.out.println("Done running " + Thread.currentThread().getId());
        }
    }


