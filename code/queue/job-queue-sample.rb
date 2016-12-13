# enqueue.rb // jobの登録
require "bundler/setup"
require "resque"

require "./job"

Resque.enqueue(Job, "Hello")


# job.rb //実行したい処理を書く
class Job
  @queue = :default
  def self.perform(message)
    sleep 10
    data = "#{message}: #{Time.now}"
    puts data
  end
end
