# coding: utf-8

class MPQueue

  def initialize
    @wcout,@wcin = IO.pipe # lock for write
    @rcout,@rcin = IO.pipe # lock for read
    @lout,@lin = IO.pipe
    @dout,@din = IO.pipe

    @wcin.syswrite(0)
    @rcin.syswrite(0)
  end

  def enq obj
    data = Marshal.dump(obj)
    
    @wcout.sysread(1) # lock write
    begin
      len = @din.syswrite data
      @lin.syswrite len.to_s + "\n"
    ensure
      @wcin.syswrite(0) # unlock write
    end
  end
  alias push enq
  alias << enq
  
  def deq
    data = ""

    @rcout.sysread(1) # lock read
    begin
      buf = ""
      len = nil
      loop do
        c = @lout.sysread(1)
        if c == "\n"
          len = buf.to_i
          break
        else
          buf << c
        end
      end

      begin
        buf = @dout.sysread(len)
        len -= buf.bytesize
        data << buf
      end while len > 0
    ensure
      @rcin.syswrite(0) # unlock read
    end
    return Marshal.load(data)
  end
  alias pop deq

end

if $0 == __FILE__
  q = MPQueue.new
  pid = fork
  if !pid
    q.enq("aaa")
    q.enq([1,2,:three])
    p q.deq
    exit(0)
  end
  p q.deq
  Process.waitall
end
