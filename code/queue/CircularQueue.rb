class CircularQueue
  def initialize(size = 32)
    @data = Array.new
    @size = size
    
    @sp = 0
    @ep = 0
  end
  
  def enqueue(data)
    if @data[@sp % @size] != nil
      puts "queue overflow"
      return
    end

    @data[@sp % @size] = data
    @sp += 1
  end
  def dequeue
    if @ep >= @sp
      puts "queue underflow"
      return
    end

    ret = @data[@ep % @size]
    @data[@ep % @size] = nil
    @ep += 1
   
    ret
  end

  def print
    for i in 0..@size-1
      puts @data[i]
    end
  end
end

q = CircularQueue.new(16)

for i in 1..16
  q.enqueue i
end

for i in 1..5
  q.dequeue
end

q.enqueue "kkk"

q.print
