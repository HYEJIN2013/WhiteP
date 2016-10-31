
public class StopWatch
{

    private long lastTime;
    private long nanoTime;
    private String name = "";

    public StopWatch( String name )
    {
        this.name = name;
    }

    public StopWatch()
    {
    }

    public StopWatch setName( String name )
    {
        this.name = name;
        return this;
    }

    public StopWatch start()
    {
        lastTime = System.nanoTime();
        return this;
    }

    public StopWatch stop()
    {
        if (lastTime < 0)
            return this;

        nanoTime += System.nanoTime() - lastTime;
        lastTime = -1;
        return this;
    }

    /**
     * @return the time delta in milliseconds
     */
    public long getTime()
    {
        return nanoTime / 1000000;
    }

    public long getNanos()
    {
        return nanoTime;
    }

    @Override
    public String toString()
    {
        String str = "";
        if (!Helper.isEmpty(name))
        {
            str += name + " ";
        }

        return str + "time:" + getSeconds();
    }

    public float getSeconds()
    {
        return nanoTime / 1e9f;
    }
}
