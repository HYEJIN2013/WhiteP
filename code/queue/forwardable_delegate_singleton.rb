
require 'singleton'
class SomeSingletonClass
  include Singleton
  attr_accessor :x
end
a = SomeSingletonClass.instance
b = SomeSingletonClass.instance  # a and b are same object
a.x = 5
p b.x # => 5

c = SomeSingletonClass.clone.instance
p c.x # => nil えっ


SomeSingletonClass.new rescue p $!
