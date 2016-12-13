
require 'forwardable'

class MyQueue
  extend Forwardable
  def initialize
    @queue = []
  end
  def_delegators :@queue , :push, :<<, :shift,
  :first, :last ,:size , :clear, :to_a
end

q = MyQueue.new
q.push 1 , 2
q << 5
p q # => #<MyQueue:0x38356f0 @queue=[1, 2, 5]>
p q.shift # => 1
p q.pop rescue p $!
