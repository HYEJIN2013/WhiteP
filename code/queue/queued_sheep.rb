require 'thread'

class Sheep
  # ...
end

sheep = Sheep.new
sheep_queue = Queue.new
sheep_queue << sheep

5.times.map do
  Thread.new do
    begin
      sheep = sheep_queue.pop(true)

      #unless sheep.shorn? - result the same!
        sheep.shear!
      #end
    rescue ThreadError
      # We moved logic here now.
      # It is not equal to "In five threads
      # sheep should shear unless shorn".
      # raised by Queue#pop in the threads
      # that don't pop the sheep
    end
  end
end.each(&:join)
