EM.run do
  queue = EM::Queue.new

  queue_work = Proc.new do |data|
    Worker.new.call(data)
    EM.next_tick { queue.pop(&queue_work) }
  end
  queue.pop(&queue_work)

  queue.push("here's some data")
end
