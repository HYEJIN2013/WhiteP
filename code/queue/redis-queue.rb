module RedisQueue
  module ActsAsQueueable

    def self.included(base)
      base.extend(ClassMethods)
    end

    module ClassMethods
      PREFIX = 'redis_queue:'

      def acts_as_queueable(options = {})
        options[:cache_prefix] ||= PREFIX + self.to_s.underscore
        raise "Please specify a primary index" unless options[:key_proc]
        options[:indexes] ||= {}
        options[:sorters] ||= {}
        options[:groups] ||= {} # coming soon

        # applies only for ActiveRecord
        options[:category_column] ||= :status if self < ActiveRecord::Base # the column to check for in order to decide whether to queue or not
        options[:enqueue_for] ||= [] # the values of the above parameter to check for in order to decide whether to queue or not

        @options = options
        queueify(options)
      end

      private
      def queueify(options)

        # applicable only for AR
        if self < ActiveRecord::Base
          raise "Column \'#{options[:category_column]}\' does not exist?" unless self.column_names.include?(options[:category_column].to_s)

          define_method :key do
            self.class.get_key(self)
          end

          define_method :_enqueue_ do

            # dequeue first
            self.class.dequeue(key)

            # now enqueue
            if options[:enqueue_for].empty?
              self.class.enqueue(self.attributes)
            elsif options[:enqueue_for].include?(self.send(options[:category_column]))
              self.class.enqueue(self.attributes, self.send(options[:category_column]))
            end
          end

          define_method :save do |*args|
            begin
              _enqueue_
            rescue Exception => e
              logger.error("RedisQueue action failed: #{e}")
            end
            super *args
          end

          define_method :_dequeue_ do
            self.class.dequeue(key)
          end

          define_method :destroy do |*args|
            begin
              _dequeue_
            rescue Exception => e
              logger.error("RedisQueue action failed: #{e}")
            end
            super *args
          end

        end

        def self.get_key(item)
          # puts @options[:key_proc].class
          if @options[:key_proc].nil?
            item
          else
            if @options[:key_proc].is_a?(String)
              item[@options[:key_proc]]
            elsif @options[:key_proc].is_a?(Proc)
              @options[:key_proc].call(item)
            else
              raise "Invalid key specification"
            end
          end
        end

        # how long does this take
        def self.rebuild_indexes
            get_queue(:page_size => 0).each do |item|
              enqueue(item)
            end
          end

        def self.flush
          # perhaps this should not use keys.grep but instead maintain a LIST of keys for this class and use smembers().each {del}
          REDIS_SERVER.keys.grep(/^#{@options[:cache_prefix]}/).each{|x| REDIS_SERVER.del(x)}
          nil
        end

        def self.dequeue(key)
          prefix = @options[:cache_prefix]
          REDIS_SERVER.smembers("#{prefix}:status:*").each do |v|
            REDIS_SERVER.zrem(v, "#{prefix}:#{key}")
          end
          REDIS_SERVER.del("#{prefix}:#{key}")
        end

        def self.queue_size(category = '')
          REDIS_SERVER.zcard("#{@options[:cache_prefix]}:#{category}")
        end
        
        def self.enqueue(o, category = '')
          data = o.to_json
          prefix = @options[:cache_prefix]
          category += ':' if category
          key = get_key(o)
          # dequeue(key)
          t = Time.now.to_i

          REDIS_SERVER.zadd("#{prefix}:#{category}", t , "#{prefix}:#{key}")
          REDIS_SERVER.zremrangebyrank("#{prefix}:#{category}", 0, -(@options[:max_size] + 1)) if @options[:max_size]
          REDIS_SERVER.sadd("#{prefix}:status:*", "#{prefix}:#{category}")
          @options[:indexes].each do |index_field, index_proc|
            index_value = index_proc.call(o)
            if index_value.is_a?(Array)
              index_value.each do |i|
                REDIS_SERVER.zadd("#{prefix}:#{index_field}:#{i}", t, "#{prefix}:#{key}")
              end
            elsif index_value.is_a?(String)
              REDIS_SERVER.zadd("#{prefix}:#{index_field}:#{index_value}", t, "#{prefix}:#{key}")
              end
            
          end
          REDIS_SERVER.set("#{prefix}:#{key}", data)
          @options[:sorters].each do |sort_field, sort_proc|
            REDIS_SERVER.set("#{prefix}:#{key}:#{sort_field}", sort_proc.call(o))
          end
        end
        
        # search functionality
        def self.get_queue(*args)
          category = nil

          options = {}
          
          # handle all kinds of argument structures that make sense
          if args.length == 1
            if args[0].is_a?(Hash)
              options = args[0]
              elsif args[0].is_a?(String)
              category = args[0]
            else
              raise
            end
          elsif args.length > 1
            category = args[0]
            options = args[1]
          end

          category += ':' if category          
          page_no = options[:page_no] || 1
          page_size = options[:page_size] || 10
          
          max_time = options[:to] || '+inf'
          min_time = options[:from] || '-inf'
          
          filters = options[:filters] || {}
          sort_by = options[:sort_by] || nil
          
          offset = (page_no - 1) * page_size
          limit = offset + page_size
          
          # search
          inter = []
          unless filters.empty?
            inter = filters.map{|k,v| "#{@options[:cache_prefix]}:#{k}:#{v}"}
          end
          
          full_list = "#{@options[:cache_prefix]}:#{category}"
          
          # get the next seq no for search operations for this search instance (perhaps this entire section shld be oops based stuff but what the heck :E mayb later)
          seq = REDIS_SERVER.incr("#{@options[:cache_prefix]}:result:seq")
          
          # is the user askin for a cropped set of data (min/max date/time of nQ)
          if min_time == '-inf' and max_time == '+inf'
            inter << full_list
          else
            # copy the full list to different temp set
            all_items_key = "#{@options[:cache_prefix]}:all_items:#{seq}"
            REDIS_SERVER.zunionstore(all_items_key, [full_list])
            REDIS_SERVER.expire(all_items_key, REDIS_TTL_SEARCH_KEYS)
            # crop the set based on min/max (wish we had a 1 step zcroprangebyscore)
            REDIS_SERVER.zremrangebyscore(all_items_key, "-inf", "(#{min_time}") if min_time != '-inf'
            REDIS_SERVER.zremrangebyscore(all_items_key, "(#{max_time}", "+inf") if max_time != '+inf'
            inter << all_items_key
          end

          result_key = "#{@options[:cache_prefix]}:result:#{seq}"
          REDIS_SERVER.zinterstore(result_key, inter, :aggregate => 'max')
          REDIS_SERVER.expire(result_key, REDIS_TTL_SEARCH_KEYS)
          result = nil
          if sort_by
            custom_sort = "#{@options[:cache_prefix]}:custom_sort:#{seq}"
            REDIS_SERVER.sort(result_key, :by => "*:#{sort_by}",:get => '*', :store => custom_sort)
            REDIS_SERVER.expire(custom_sort, REDIS_TTL_SEARCH_KEYS)
            result = REDIS_SERVER.lrange(custom_sort, offset, limit -1)
          else
            res_keys = REDIS_SERVER.zrevrange(result_key, offset, limit - 1)
            if res_keys.empty?
              result = []
            else
              result = REDIS_SERVER.mget(*res_keys)
            end
          end
          result.compact.map{|x| JSON.parse(x) rescue x}
        end
      end
      
    end
  end
end

ActiveRecord::Base.send(:include, RedisQueue::ActsAsQueueable)

# example usage

class MyQueue
  include RedisQueue::ActsAsQueueable
  acts_as_queueable(:key => 'id', :indexes => ['first_name', 'last_name'])

end

MyQueue.enqueue({'id' => 1, 'first_name' => 'Schubert', 'last_name' => 'Cardozo'})
MyQueue.enqueue({'id' => 2, 'first_name' => 'John', 'last_name' => 'Doe'})
MyQueue.enqueue({'id' => 3, 'first_name' => 'John', 'last_name' => 'Smoe'})
MyQueue.enqueue({'id' => 4, 'first_name' => 'Don', 'last_name' => 'Joe'})
MyQueue.enqueue({'id' => 5, 'first_name' => 'John', 'last_name' => 'Moe'})
MyQueue.enqueue({'id' => 6, 'first_name' => 'John', 'last_name' => 'Foe'})
MyQueue.enqueue({'id' => 7, 'first_name' => 'Don', 'last_name' => 'Loe'})
MyQueue.enqueue({'id' => 8, 'first_name' => 'Von', 'last_name' => 'Toe'})
MyQueue.enqueue({'id' => 9, 'first_name' => 'John', 'last_name' => 'Woe'})

# get the first 10
MyQueue.get_queue

# get the entire queue
MyQueue.get_queue(:page_size => 0)

# get page no 2 by pagination of 4
MyQueue.get_queue(:filters => {'first_name' => 'John'}, :page_size => 4, :page_no => 2)
