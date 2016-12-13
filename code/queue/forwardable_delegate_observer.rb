require "observer"
require "dxruby"

class Observer
  include Observable
end
class O
 attr_accessor :sym , :x , :y , :d
 def initialize sym , x , y , d
   @x     = x
   @y     = y
   @d     = d
   @sym   = sym
   @func  = proc
 end
 def update *h
   @func.call self
   Window.draw x , y , d
 end
end
task    = Observer.new
us_task = Observer.new
task.add_observer O.new :user , 200 , 300 , Image.new(50,50,[200,210,160]) , &->o do
  o.x += Input.x * 4
  o.y += Input.y * 4
  if Input.keyPush? K_Z
    us_task.add_observer O.new :user_shot , o.x , o.y , Image.new(10,5,[200,210,160]) , &->o do
      if ( o.y -= 3 ) < 0
        us_task.delete_observer o
      end
    end
  end
end

Window.loop do
  exit if Input.keyPush? K_F9
  task.changed
  task.notify_observers
  us_task.changed
  us_task.notify_observers

  Window.drawFont 50 , 50 ,    task.count_observers.to_s , Font.default
  Window.drawFont 50 , 80 , us_task.count_observers.to_s , Font.default
end
