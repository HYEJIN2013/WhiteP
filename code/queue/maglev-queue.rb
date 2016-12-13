require 'maglev/rcqueue'

Store = Maglev::PERSISTENT_ROOT

Maglev.abort_transaction

Store[:queue] ||= RCQueue.new

20.times do |t|
  Store[:queue] << Proc.new do
    sleep 1
    puts "job ##{t}"
  end
end

Maglev.commit_transaction

loop do
  Maglev.abort_transaction
  
  until Store[:queue].empty?
    Thread.new do
      Store[:queue].shift.call
    end
    
    Maglev.commit_transaction
  end
  
  sleep 0.5
end
