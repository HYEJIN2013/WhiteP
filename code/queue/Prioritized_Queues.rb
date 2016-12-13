require 'eventmachine'
#
module EventMachine
  class EventQueuePool
    def initialize(settings={}, total_slots=10)
      @scheduled = false
      @event_count = 0
      @slots = 0
      @queue_pool = {:main => []}
      @allocations = {:main => total_slots}
      used_slots = 0
      new_allocations = {}
      if settings.keys.size > 0
        frame_slots = (total_slots.to_f / (settings.keys.size + 1).to_f).to_i
        EM::Iterator.new(settings.keys, 1).each do |q_id, iter|
          tick_times = (((settings[(q_id)]).to_f / 100.00) * frame_slots.to_f).to_i
          new_allocations[(q_id.to_sym)] = tick_times
          @queue_pool[(q_id.to_sym)] = []
          used_slots += tick_times
          iter.next
        end
        if used_slots < total_slots
          if used_slots > 0
            new_allocations[:main] = total_slots - used_slots
          else
            new_allocations[:main] = 1
          end
        else
          new_allocations[:main] = 1
        end
      end
      #
      if new_allocations.keys.size > 0
        @allocations = new_allocations
      end
      #
      EM::Iterator.new(@allocations.values, 1).each do |slot_set, iter|
        @slots += slot_set
        iter.next
      end
    end
    #
    def post_event(inputs = {})
        inputs = {:queue => :main}.merge(inputs)
        # inputs should be : {:queue => :sym_name, :callback => Proc}
        if @queue_pool[(inputs[:queue].to_sym)]
          cb = nil
          if inputs[:callback].is_a?(Proc)
              cb = inputs[:callback]
          else
            raise "invalid callback supplied -- pass a Proc; you passed #{inputs[:callback].inspect}"
          end
          #
          EM.schedule do
            # post changes to queues here
            if cb
            @queue_pool[(inputs[:queue].to_sym)] << cb
              @event_count += 1
              unless @scheduled
                @scheduled = true
                EM::next_tick( Proc.new { self.schedule_events } )
              end
            end
          end
          #
        else
          raise "Event Queue :#{inputs[:queue].to_s} not found."
        end
    end
    #
    def schedule_events()
      #
      EM.schedule do
        q_alloc = @allocations.clone
        EM::Iterator((1..(@slots)),1).each do |slot, outer_iter|
          EM::Iterator(q_alloc.keys,1).each do |q_id, iter|
            if q_alloc[(q_id)] > 0
              cb = @queue_pool[(q_id)].shift
              if cb
                q_alloc[(q_id)] = q_alloc[(q_id)] - 1
                @event_count -= 1
                EM::next_tick(cb)
                #
              end
            end
            iter.next
          end
          outer_iter.next
        end
        if @event_count > 0
          @scheduled = true
          EM::next_tick( Proc.new { self.schedule_events } )
        else
          @scheduled = false
        end
      end
      #
    end
  end
end
#
