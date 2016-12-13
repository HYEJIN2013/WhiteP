require 'forwardable'

class WeleStack
  extend Forwardable

  def initialize(obj=[])
    @queue = obj
  end

  def_delegator :@queue, :push, :empuja
  def_delegator :@queue, :shift, :quita

  def_delegators :@queue, :clear, :empty?, :length, :size, :<<

end
