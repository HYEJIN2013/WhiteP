class PQueue
  def initialize
    @a = []
    @heapsize = 0
  end

  def left(i)
    2 * i + 1
  end

  def right(i)
    2 * i + 2
  end

  def parent(i)
    i / 2
  end

  def heapify(i, heapsize)
    l = left(i)
    r = right(i)
    largest = i

    largest = l if l < heapsize && @a[l] > @a[largest]
    largest = r if r < heapsize && @a[r] > @a[largest]

    if largest != i
      @a[i], @a[largest] = @a[largest], @a[i]
      heapify(largest, heapsize)
    end
  end

  def maximum
    return @a[0]
  end

  def extract
    return nil if @heapsize < 1
    max = @a[0]
    @a[0] = @a[@heapsize - 1]
    @heapsize -= 1
    heapify(0, @heapsize)
    return max
  end

  def increase_key(i, key)
    return if @a[i].nil? or key < @a[i]
    @a[i] = key
    while i > 0 and @a[parent(i)] < @a[i]
      @a[i], @a[parent(i)] = @a[parent(i)], @a[i]
      i = parent(i)
    end
  end

  def insert(key)
    @heapsize = @heapsize + 1
    @a[@heapsize - 1] = -1.0 / 0.0
    increase_key(@heapsize - 1, key)
  end
end

p = PQueue.new

[15,13,9,5,12,8,7,4,0,6,2,1].each { |v| p.insert(v) }
