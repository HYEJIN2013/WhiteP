
redis = Redis.current
key = "resque:queue:bulk"
total = redis.llen(key)

batch = []
total.times do |i|
  entry = redis.lpop(key)
  batch << entry
  if batch.size == 1000
    puts "re-inserting batch..."
    redis.rpush key, batch.shuffle
    batch = []
  end
end
