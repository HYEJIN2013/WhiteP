# Add more tasks from another instance of maglev irb:

Store = Maglev::PERSISTENT_ROOT

Maglev.abort_transaction

5.times do
  Store[:queue] << Proc.new do
    sleep 1
    puts 'another task!'
  end
end

Maglev.commit_transaction
