# encoding: utf-8

require 'redis'
require 'redis/connection/hiredis'

class RedisQueue
  attr_reader :redis, :queue, :buffer, :timeout
  attr_accessor :buffer_max

  def initialize(queue_name, options = {})
    if !queue_name.is_a?(String) || queue_name.empty?
      raise ArgumentError, "Queue name must be a non empty string"
    end

    @queue      = "#{queue_name}:source"
    @buffer     = "#{queue_name}:buffer"
    @redis      = options.fetch(:redis, Redis.current)
    @buffer_max = options.fetch(:conc_num, 8)
  end

  # Return the buffer max num
  #
  # @return [int]
  alias :conc_num :buffer_max

  # Reset the buffer max num
  #
  # @return [int]
  alias :conc_num= :buffer_max=

  # Returns the number of queue elements
  #
  # @return [int]
  def length
    redis.llen(queue)
  end
  alias :size :length

  # Checks whether the queue is empty
  #
  # @return [true, false]
  def empty?
    !(length > 0)
  end
  alias :empty :empty?

  # Access the first element of queue
  #
  # @return [Object]
  def front
    redis.lindex(queue, 0)
  end

  # Access the last element of queue
  #
  # @return [Object]
  def back
    redis.lindex(queue, -1)
  end

  # Access all elements of queue
  #
  # @return [List of Object]
  def list
    redis.lrange(queue, 0, -1)
  end

  # Access all elements of buffer
  #
  # @return [List of Object]
  def runners
    redis.lrange(buffer, 0, -1)
  end

  # Removes the first element of queue and push it to buffer
  # if the buffer is fill, return nil
  #
  # @return [Object]
  def pop
    redis.rpoplpush(queue, buffer) unless buffer_is_fill?
  end

  # Inserts element at the end of queue and return the size of queue
  #
  # @return [int]
  def push(obj)
    redis.lpush(queue, obj)
  end
  alias :<< :push

  # Remove one element of queue
  # return false if the element not exist
  #
  # @return [true, false]
  def remove(obj)
    (redis.lrem(queue, 1, obj) != 0) ? true : false
  end
  alias :delete :remove

  # Remove one element of buffer
  # return false if the element not exist
  #
  # @return [true, false]
  def commit(obj)
    (redis.lrem(buffer, 1, obj) != 0) ? true : false
  end

  # Clear the queue and buffer
  def clear
    redis.del(queue)
    redis.del(buffer)
  end

  private

  def buffer_is_fill?
    redis.llen(buffer) >= buffer_max
  end
end
