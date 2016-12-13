require 'thread'

q = Queue.new
(0..1000).each{ |i| q << i }
puts q.length

Thread.new do
  sleep 1
  puts "FIRST #{q.pop}"
end

Thread.new do
  loop do
    sleep 1
    puts "SECOND #{q.pop}"
  end
end

sleep 5
