require 'thread'

class QuWk
  NUM = 3

  def initialize
    @queue = Queue.new
    @workers = []
    @num = NUM
    @block = proc {}
  end

  def close
    NUM.times { @queue.push nil }
    @workers.each(&:join)
  end

  def push(item)
    @queue.push item
  end

  def register(&block)
    @block = block
  end

  def perform
    @num.times do |number|
      worker = Thread.new(@queue, @block) do |queue, block|
        while item = queue.pop
          block.call item
        end
      end
      worker[:number] = number
      @workers.push worker
    end
  end
end
