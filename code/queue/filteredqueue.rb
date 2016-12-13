#!/usr/bin/env ruby

require 'thread'

class FilteredQueue < Queue
  attr_accessor :push_filter, :pop_filter

  def initialize(internal_data)
    super()
    @internal_data = internal_data
    @push_filter = nil
    @pop_filter = nil
  end

  def push(obj)
    @mutex.synchronize{
      return if @push_filter && !@push_filter.call(obj, @internal_data)
      return if block_given? && !yield(obj, @internal_data)

      @que.push obj
      begin
        t = @waiting.shift
        t.wakeup if t
      rescue ThreadError
        retry
      end
    }
  end

  def pop(non_block=false)
    obj = @mutex.synchronize{
      while @que.empty?
        raise ThreadError, "queue empty" if non_block
        @waiting.push Thread.current
        @mutex.sleep
      end

      @que.shift
    }

    begin
      if @pop_filter && !@pop_filter.call(obj, @filter_data)
        @mutex.synchronize{
          @que.unshift(obj)
        }
        return nil
      end
      if block_given? && !yield(obj, @filter_data)
        @mutex.synchronize{
          @que.unshift(obj)
        }
        return nil
      end
    rescue Exception => e
      @mutex.synchronize{
        @que.unshift(obj)
      }
      raise e
    end

    return obj
  end

  def values
    return @que.clone
  end

end

if $0 == __FILE__
  q = FilteredQueue.new({})
  def q.dump
    return "#{@que.length}: #{@que.join(', ')}"
  end
  q.push_filter = Proc.new {|value, hash|
    raise TypeError if hash.key?(value)
    hash[value] = true
  }
  q.pop_filter = Proc.new {|value, hash|
    true
  }

  puts "Start"
  puts "\t" + q.dump

  puts "Try to push 5 non-filtered values"
  q.push(1) rescue TypeError
  q.push(2) rescue TypeError
  q.push(3) rescue TypeError
  q.push(10) rescue TypeError
  q.push(20) rescue TypeError
  puts "\t" + q.dump

  puts "Try to push 3 filtered values"
  q.push(2) rescue TypeError
  q.push(10) rescue TypeError
  q.push(99) do |value, hash|
    false
  end rescue TypeError
  puts "\t" + q.dump

  puts "Try to push 3 non-filtered values"
  q.push(4) rescue TypeError
  q.push(30) rescue TypeError
  q.push_filter = nil
  q.push(99) do |value, hash|
    true
  end rescue TypeError
  puts "\t" + q.dump

  puts "Try to pop non-filtered value x2 times"
  q.pop
  q.pop do |value, hash|
    true
  end
  puts "\t" + q.dump

  puts "Try to pop an filtered value x2 times"
  q.pop do |value, hash|
    false
  end
  q.pop do |value, hash|
    raise TypeError(value)
  end rescue TypeError
  puts "\t" + q.dump

  puts "Try to pop an non-filtered value x2 times"
  q.pop
  q.pop do |value, hash|
    true
  end rescue TypeError
  puts "\t" + q.dump
end
