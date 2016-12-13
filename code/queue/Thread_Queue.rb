require 'thread'
queue = Queue.new
Thread.new do
 100.times do |i|
   sleep 1
   queue.enq i
 end
end

loop do
 print "waiting... "
 puts queue.deq      # this function blocks.
end
