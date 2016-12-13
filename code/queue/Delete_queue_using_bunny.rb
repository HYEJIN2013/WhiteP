require 'bunny'
def delete_queue(queue_name)
  Bunny.run(MessagingHelper.config.amqp) do |bunny|
    queue = bunny.queue(queue_name, {:durable => true})
    queue.delete
  end
end
