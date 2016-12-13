queue_name = 'queue:queue_name'
len = Resque.redis.llen(queue_name)

deletion = Resque.redis.lrange(queue_name,0, len).select do |entry|
  JSON.parse(entry)['args'][0] == "some_criterial" rescue nil
end

deletion.each do |entry|
  puts entry
  puts Resque.redis.lrem queue_name, -1, entry
end
