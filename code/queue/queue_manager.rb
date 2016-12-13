require 'bunny'

class QueueManager
  
  attr_reader :bunny, :bunny_exchange
  
  def initialize(settings)
    @bunny = Bunny.new(settings)
    @bunny.start
    @bunny_exchange = @bunny.exchange('', :durable => false)
    @queue_names = []
    return self
  end
  
  def message_count(queue_name)
    my_queue = @bunny.queue(queue_name)
    return my_queue.message_count
  end
  
  def push(queue_name, msg)
    my_queue = @bunny.queue(queue_name)
    @bunny_exchange.publish(serialize(msg), :key => my_queue.name)
    return my_queue.message_count
  end
  
  def pop(queue_name)
    return deserialize(@bunny.queue(queue_name).pop[:payload])
  end
  
  def stop
    @bunny.stop
  end
  
  def stats(queue_names=[])
    queue_names.each {|queue_name| message_count(queue_name)}
    hsh = {}
    @bunny.queues.each do |queue_name, queue|
      hsh[queue_name] = queue.message_count
    end
    
    return hsh
  end
  
  def stats_pretty(queue_names=[])
    ret = []
    stats(queue_names).keys.sort.each do |queue_name|
      ret << "#{queue_name}\t#{stats[queue_name]}"
    end

    return ret.join("\n")
  end
  
  def queue_exists?(queue_name)
    @bunny.queues.keys.include?(queue_name)
  end
  
  def drop_queue(queue_name)
    if queue_exists?(queue_name)
      @bunny.queues[queue_name].delete
    else
      nil
    end
  end
  
  private
  
    def serialize(object)
      return Marshal::dump(object)
    end
    
    def deserialize(serialized_object)
      return serialized_object if serialized_object.is_a? Symbol
      return nil if serialized_object.blank?
      return Marshal::load(serialized_object)
    end
end
