
# -*- encoding: sjis -*-

FIZZ = __FILE__.to_s[0..3]
BUZZ = __FILE__.to_s[4..7]

class PriI
  def print(i)
    i.to_s
  end
end

class PriFizz
  def print(i)
    FIZZ.to_s
  end
end

class PriBuzz
  def print(i)
    BUZZ.to_s
  end
end

class PriFizzBuzz
  def print(i)
    FIZZ.to_s + BUZZ.to_s
  end
end

class Queue
  def initialize
    @n = -1
    @array = [PriI.new, PriI.new, PriFizz.new, PriI.new, PriBuzz.new,
           PriFizz.new, PriI.new, PriI.new, PriFizz.new, PriBuzz.new,
           PriI.new, PriFizz.new, PriI.new, PriI.new, PriFizzBuzz.new]
  end
  
  def pop
    @n += 1
    if @n >= 15
      @n -= 15
    end
    return @array[@n]
  end
  
end

queue = Queue.new

1.upto(20){|n|
  puts queue.pop.print(n)
}
