# Solution to 'Queue Continuum' on rubeque.com
# by jakthegr8
# http://www.rubeque.com/problems/queue-continuum

class Queue
  def initialize(arr)
  @arr = arr
end
def pop(*idx)
  @arr.shift *idx
end
def push(elem)
  @arr.push(*elem) == @arr
end
def to_a
  @arr
end
end

queue = Queue.new([5, 6, 7, 8])

assert_equal queue.pop, 5
assert_equal queue.pop, 6
assert_equal queue.push([4, 2]), true
assert_equal queue.pop(2), [7, 8]
assert_equal queue.to_a, [4, 2]
