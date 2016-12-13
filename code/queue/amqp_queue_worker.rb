require "rubygems"
require "amqp"

EventMachine.run do
  connection = AMQP.connect(:host => '127.0.0.1')
  channel_low  = AMQP::Channel.new(connection)
  channel_high  = AMQP::Channel.new(connection)

  # Attempting to set the prefetch higher on the high priority queue
  channel_low.prefetch(10)
  channel_high.prefetch(20)

  low_queue    = channel_low.queue("low", :auto_delete => false)
  high_queue    = channel_high.queue("high", :auto_delete => false)

  low_queue.subscribe do |payload|
    puts "#{payload}"
    slow_task
  end

  high_queue.subscribe do |payload|
    puts "#{payload}"
    slow_task
  end

  def slow_task
    # Do some slow work
    sleep(1)
  end
end
