class BlockQueue
  def initialize
    @storage = []
    @mutex = Mutex.new
  end

  def push(value)
    @mutex.synchronize do
      @storage.push(value)
    end
  end

  def pop
    @mutex.synchronize do
      @storage.shift
    end
  end
end
