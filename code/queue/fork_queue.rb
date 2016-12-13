#!/usr/bin/env ruby

require 'redis'

class Supervisor
  PRE_FORKS = 5

  def initialize
    @workers = []
    $0 = "Paperless-Worker (Supervisor)"
  end

  def spawn_worker
    worker = Worker.new
    @workers << worker
    worker.spawn
  end

  def spawn_workers
    while @workers.length < (PRE_FORKS+1)
      spawn_worker
    end
  end

  def watch_workers
    loop{
      Signal.trap('CLD') {
        begin
          @workers.delete(find_worker_by_pid(Process.wait))
        rescue Errno::ECHILD
        end
        spawn_worker
      }
      logger.info "Supervisor #{Process.pid}: #{@workers.length} Workers"
      spawn_workers if @workers.length < PRE_FORKS
      sleep 1
    }
  end

  def find_worker_by_pid(pid)
    @workers.select{|w| w.pid == pid}[0]
  end

  def logger
    @logger ||= Logger.new(STDOUT)
  end

  def to_s
    "#<Supervisor:#{self.object_id} @workers=#{@workers}>"
  end
end

require 'logger'

class Worker
  def initialize
     @redis = Redis.new
  end

  def pid
    @pid
  end

  def logger
    @logger ||= Logger.new(STDOUT)
  end

  def spawn
    @pid = fork{
      $0 = "Paperless-Worker (Worker)"
      @pid = Process.pid
      logger.info "Started worker with pid #{Process.pid}"
      start
    }
    @pid
  end

  def start
    sleep 1
    logger.info self
    exit
  end

  def to_s
    "#<Worker:#{self.object_id} @pid=#{@pid}>"
  end
end

s = Supervisor.new
s.spawn_workers
s.watch_workers
