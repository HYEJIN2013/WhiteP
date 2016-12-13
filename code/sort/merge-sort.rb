class Array
  def self.split(array)
    left = []
    right = []
    length = array.length
    if length.odd?
      left = array.first(length / 2 + 1)
    else  
      left = array.first(length / 2)
    end
    right = array.last(length / 2)
    return [left, right]
  end
  
  def self.merge(first, second)
    if second.empty?
      return first.dup
    elsif first.empty?
      return second.dup 
    elsif first[0] < second[0]
      [first[0]] + merge(first[1..-1], second)
    else
      [second[0]] + merge(first, second[1..-1])
    end
  end

  def self.mergesort(array)
    left = []
    right = []

    if array.length <= 1
      return array
    else
      split = Array.split(array)
      left = mergesort(split[0])
      right = mergesort(split[1])
      return Array.merge(left, right)
    end
  end
end
