require 'thread/pool'

class ClearhausQueueRunner
  attr_reader :logger, :interrupt

  def initialize(options = {})
    @logger      = options[:logger] || construct_logger
    @interrupt   = options[:interrupt] || OpenStruct.new(stopped: false, reload: false)
  end

  def consumer
    @consumer ||= ClearhausBackend::QueueConsumer.new
  end

  def concurrency
    SETTINGS[:queue][:workers] || 1
  end

  def pool
    @pool ||= Thread.pool(0, concurrency)
  end

  def run
    at_exit { pool.shutdown }

    until interrupt[:stopped]
      resize_workers
      pool.process { work }
      sleep(0.05)
    end
  end

  def resize_workers
    if interrupt[:reload]
      SETTINGS.reload
      pool.resize(0, concurrency)
      interrupt[:reload] = false
    end
  end

  def work
    consumer.consume
  rescue => e
    logger.thrown("Error", e)
  end
end


## for Daemon
queue_daemon.try_try_daemonize do
  interrupt = OpenStruct.new(stopped: false, reload: false)
  Signal.trap('USR2'){ interrupt.reload = true }
  Signal.trap('TERM'){ interrupt.stopped = true }
  
  runner = ClearhausQueueRunner.new(interrupt: interrupt)
  runner.run
  
  ...
end
