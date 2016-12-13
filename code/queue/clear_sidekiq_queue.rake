class SidekiqUtil

  def self.queues
    ::Sidekiq::Stats.new.queues.keys.map { |name| ::Sidekiq::Queue.new(name) }
  end

  def self.clear_all
    self.queues.each { |q| q.clear }
  end

end

namespace :jobs do
  desc "Clear out the sidekiq job queue"
  task :clear_sidekiq_queue, [:frequency] => :environment do |t, args|
    SidekiqUtil.clear_all
  end
end
