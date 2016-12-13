require 'benchmark'

require 'aws'
require 'beanstalk-client'
require 'carrot'
require 'iron_mq'

require_relative 'config.rb'

msg = "a"*1000

Benchmark.bm do |b|
  beanstalk = Beanstalk::Connection.new("#{IRON_HOST}:#{IRON_BEANSTALKD_PORT}")
  beanstalk.put("oauth #{IRON_TOKEN} #{IRON_PROJECT_ID}")
  beanstalk.use(QUEUE)

  b.report("IronMQ Beanstalkd push") do
    N_ITEMS.times { beanstalk.put(msg) }
  end

  beanstalk.watch(QUEUE)
  b.report("IronMQ Beanstalkd pop") do
    N_ITEMS.times {
      job = beanstalk.reserve
      job.delete
    }
  end
  beanstalk.close

  iron_client = IronMQ::Client.new(
    token: IRON_TOKEN,
    project_id: IRON_PROJECT_ID,
    queue_name: QUEUE,
    host: IRON_HOST,
    port: IRON_HTTP_PORT,
  )
  iron_messages = iron_client.messages

  b.report("IronMQ HTTP push") do
    N_ITEMS.times { iron_messages.post(msg) }
  end

  b.report("IronMQ HTTP pop") do
    N_ITEMS.times {
      job = iron_messages.get
      job.delete
    }
  end

  beanstalk = Beanstalk::Connection.new("#{BEANSTALKD_HOST}:#{BEANSTALKD_PORT}")
  beanstalk.use(QUEUE)

  b.report("Beanstalkd push") do
    N_ITEMS.times { beanstalk.put(msg) }
  end

  beanstalk.watch(QUEUE)
  b.report("Beanstalkd pop") do
    N_ITEMS.times {
      job = beanstalk.reserve
      job.delete
    }
  end
  beanstalk.close

  sqs = Aws::Sqs.new(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
  q = sqs.queue(QUEUE)

  b.report("Amazon SQS push") do
    N_ITEMS.times { q.send_message(msg) }
  end

  b.report("Amazon SQS pop") do
    N_ITEMS.times {
      job = q.receive_messages
      job.delete
    }
  end

  rabbitmq = Carrot.new(
    host: RABBITMQ_HOST,
    port: RABBITMQ_PORT,
  )
  q = rabbitmq.queue(QUEUE, durable: true)

  b.report("RabbitMQ push") do
    N_ITEMS.times { q.publish(msg) }
  end

  b.report("RabbitMQ pop") do
    N_ITEMS.times { q.pop }
  end

  Carrot.stop
end
