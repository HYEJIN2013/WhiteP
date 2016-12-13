require 'thread'

class MisoQueueQueue

  def initialize misoque
    @misoque = misoque
  end

  def push obj
    @misoque.push self,obj
  end
  alias << push
  alias enq push

end

class MisoQueue

  def initialize
    @mutex = Mutex.new
    @ques = {}
    @arrival = []
    @waiting = []
  end

  def new_queue
    que = MisoQueueQueue.new(self)
    @ques[que] = []
    return que
  end
  alias new_que new_queue

  def push que,obj
    @mutex.synchronize{
      @ques[que].push obj
      @arrival.push que
      begin
        t = @waiting.shift
        t.wakeup if t
      rescue ThreadError
        retry
      end
    }
  end

  def pop(non_block=false)
    @mutex.synchronize{
      while true
        if @arrival.empty?
          raise ThreadError, "queue empty" if non_block
          @waiting.push Thread.current
          @mutex.sleep
        else
          que = @arrival.shift
          return que,@ques[que].shift
        end
      end
    }

  end
  alias deq pop
  alias shift pop

end

if __FILE__ == $0
  misoque = MisoQueue.new
  q1 = misoque.new_queue
  q2 = misoque.new_queue

  Thread.new{
    loop do
      que,obj = misoque.pop
      case que
      when q1
        puts "*q1"
      when q2
        puts "*q2"
      end
      puts obj
      puts
    end
  }

  sleep 1
  q1.push "q1:1"
  q2.push "q2:1"
  sleep 1
  q2.push "q2:2"
  q1.push "q1:2"
  sleep 1

end
