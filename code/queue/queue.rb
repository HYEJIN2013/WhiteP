class Queue
  def initialize(max_size)
    @store = []
    @max_size = max_size
  end

  def enqueue(x)
    if full?
      raise "Queue is full"
    else
      @store.push x
    end
  end

  def dequeue
    raise "Queue Underflow - The Queue is empty" if self.empty?
    @store.shift
  end

  def peek
    @store.first
  end

  def empty?
    @store.empty?
  end

  def full?
    @store.length == @max_size
  end
end

my_queue = Queue.new(5)

my_queue.empty?

my_queue.enqueue("ruby")
my_queue.enqueue("is")
my_queue.enqueue("cool")

p my_queue.dequeue
