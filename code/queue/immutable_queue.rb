class ImmutableQueue
  attr_reader :first, :last, :count
  def initialize
    @count = 0
  end

  def << object
    object = object.dup rescue object
    node = Node.new(object)
    duplicate do
      if first
        @last.next = node
        @last = node
      else
        @first = node
        @last = node
      end
      @count += 1

      self
    end
  end

  def empty?
    count == 0
  end

  def pop
    popped = first.object
    new_queue = duplicate do
      @first = first.next
      @last = first unless first
      @count -= 1
    end

    [popped, new_queue]
  end

  def peek
    first.object
  end

  def == other
    return false unless other.is_a?(self.class) && other.count == count
    current = first
    other_current = other.first
    loop do
      return true if current.nil?
      return false if current.object != other_current.object
      current = current.next
      other_current = other_current.next
    end
  end

  class Node
    attr_reader :object
    attr_accessor :next
    def initialize object
      @object = object
    end

    def == other
      other.is_a?(self.class) && other.object == object
    end
  end

  private

  def duplicate &block
    duplicate = dup
    duplicate.instance_exec(&block)
    duplicate
  end
end
