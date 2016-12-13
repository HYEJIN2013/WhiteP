queues = []
queues << queue_consumer("high")
queues << queue_consumer("normal")

def next_message
  # look for a message from each queue in priority order
  queues.each do |queue|
    found, message = queue.non_blocking_dequeue
    return [found, message] if found
  end

  # block on the highest priority queue for a while to avoid pounding
  # what is a sensible time depends on your case
  queues.first.blocking_dequeue(500ms)
end

while true do # make this a changeable flag to stop consuming gracefully
  found, message = next_message

  if found
    process_message(message)
    ack_message(message)
  end
end
