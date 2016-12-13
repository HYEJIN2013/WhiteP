class PriorityQueue
  def initialize
    @pq = []
    @sorted = true
  end

  def push(object, priority)
    @pq << [ object, priority ]
    @sorted = false
  end

  def force_sort
    if not @sorted
      @pq = @pq.sort_by {|l| l[1] }
      @sorted = true
    end
  end

  def pop
    force_sort
    @pq.pop[0] rescue nil
  end

  def peek
    force_sort
    @pq[-1][0] rescue nil
  end

  def length
    @pq.length
  end
end

if __FILE__ == $0
  $results = []
  def assert(bool)
    $results << bool
  end

  $pq = PriorityQueue.new
  $pq.push("highest priority", 10)
  $pq.push("medium priority", 5)
  $pq.push("low priority", 1)
  assert $pq.peek == "highest priority"
  assert $pq.pop == "highest priority"
  assert $pq.length == 2
  $pq.push("medium-low priority", 3)
  assert $pq.pop == "medium priority"
  assert $pq.pop == "medium-low priority"
  assert $pq.pop == "low priority"
  assert $pq.pop == nil
  
  passedl = $results.select {|i| i }
  passedn = passedl.length
  passedg = (passedl.map {|i| i ? '-' : '#'}).join
  puts "#{passedn}/#{$results.length} tests passed. (#{passedg})"
end
