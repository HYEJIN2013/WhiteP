require 'queue_manager'
  
namespace :queue do
  
  desc 'Spawn multiple RabbitMQ consumer workers'
  task :workers => :environment do
    threads = []
    
    queue_name = ENV['QUEUE']
    num_workers = ENV['COUNT'] ||= '1'
    
    if queue_name.blank?
      puts "\nUsage: rake queue:workers QUEUE='queue_name' COUNT=3\n\n"
      exit 0
    end

    num_workers.to_i.times do
      threads << Thread.new do
        system "rake queue:worker QUEUE='#{queue_name}'"
      end
    end

    threads.each { |thread| thread.join }
  end
  
  desc "Run the RabbitMQ consumer worker"
  task :worker => :environment do
    queue_manager = QueueManager.new(AMQP_CONFIG)
    queue_name = ENV['QUEUE']
    
    if queue_name.blank?
      puts "\nUsage: rake queue:worker QUEUE='queue_name'\n\n"
      exit 0
    end
    
    sleep_time = 1
    while true
      popped_message = queue_manager.pop(queue_name)
      if popped_message == :queue_empty
        sleep(sleep_time)
      else
        if popped_message.respond_to?(:perform)
          t1 = Time.now
          begin
            popped_message.perform
          rescue => ex
            QUEUE_LOGGER.error "[#{Time.now.strftime('%Y-%m-%d %H:%I:%S')}] Error Thrown: #{ex.message}"
            ex.backtrace.each do |line|
              QUEUE_LOGGER.error "> #{line}"
            end
          ensure
            t2 = Time.now
            QUEUE_LOGGER.debug "[#{Time.now.strftime('%Y-%m-%d %H:%I:%S')}] #{popped_message.class} completed with options #{popped_message.options.to_json} in #{t2-t1} seconds\n"
          end
        else
          msg = """
          ** Queue with name '#{queue_name}' must be added to config/initializers/load_amqp_config.rb
          Payload:\n\n#{popped_message.inspect}\n\n
          """
          QUEUE_LOGGER.error "[#{Time.now.strftime('%Y-%m-%d %H:%I:%S')}] #{msg}"
        end
      end
    end
    
    queue_manager.stop
  end
  
end
