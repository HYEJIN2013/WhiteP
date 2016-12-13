class MyQueue
  attr_accessor :size

  def initialize
    @size = 0
    @items = []
  end

  def is_empty?
    @size == 0
  end

  def enqueue(item)
    @items << item 
    @size += 1
    @items
  end

  def peek
    @items[0]
  end

  def dequeue
    if is_empty? == false 
      item = @items.delete_at(0)
      @size -= 1
      item
    else
      nil
    end

  end
end
