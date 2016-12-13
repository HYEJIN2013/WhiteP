class Queue
  def initialize
    @store = []
    @max_size=12
  end

  def enqueue(x)
    if @store.count<@max_size
      @store.push x
    else
      raise "Sorry, queue Overflow"
    end
  end

  def dequeue
    raise "Queue Underflow - The queue is empty" if self.empty?
    @store.shift
  end

  def peek
    @store.first
  end

  def empty?
    @store.empty?
  end

  def full?
    @store.count>=@max_size ? true : false
  end
end

my_queue=Queue.new

my_queue.enqueue("first customer")
my_queue.enqueue("second customer")
my_queue.enqueue("third customer")
my_queue.enqueue("fourth customer")
my_queue.enqueue("fifth customer")
p "peeking at front of the line #{my_queue.peek}"
my_queue.enqueue("sixth customer")
my_queue.enqueue("seventh customer")
my_queue.enqueue("eighth customer")
my_queue.enqueue("nineth customer")
p my_queue.full? ==false
my_queue.enqueue("tenth customer")
my_queue.enqueue("eleventh customer")
my_queue.enqueue("last customer")
p my_queue.full? ==true
p my_queue.dequeue =="first customer"
p "peeking at front of the line #{my_queue.peek}"
p my_queue.full? ==false
my_queue.enqueue("that customer")
my_queue.full? ==true
my_queue.enqueue("that other customer")
