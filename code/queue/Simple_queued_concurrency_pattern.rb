class AsyncPool
  def initialize
    @threads = {}
    @results = {}
  end

  def run(id, &block)
    @threads[id] = Thread.new { @results[id] = block.call }
  end

  def result(id)
    @threads[id].join
    @results[id]
  end
end


pool = AsyncPool.new

pool.run(:one)    { sleep 2; "one" }
pool.run(:two)    { sleep 4; "two" }
pool.run(:three)  { sleep 8; "three" }

puts pool.result(:two)
puts pool.result(:one)
puts pool.result(:three)
