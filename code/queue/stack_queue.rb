require 'thread'
# Borrowed from https://github.com/ruby/ruby/blob/ruby_1_9_3/lib/thread.rb#L140
# and modified for a last in first out processing
#
#
class StackQueue < Queue
  # Last in first out Queue
  #
  # Retrieves data from the queue. If the queue is empty, the calling thread is
  # suspended until data is pushed onto the queue. If +non_block+ is true, the
  # thread isn't suspended, and an exception is raised.
  #
  def pop(non_block=false)
    @mutex.synchronize{
      while true
        if @que.empty?
          raise ThreadError, "queue empty" if non_block
          @waiting.push Thread.current
          @mutex.sleep
        else
          return @que.pop # was shift
        end
      end
    }
  end
end
