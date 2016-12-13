require 'mysql2-cs-bind'

def get_db
  return Mysql2::Client.new(
    :host => 'localhost',
    :port => 3306,
    :username  => 'root',
    :password  => '',
    :database  => 'queue_test',
    :reconnect => true,
  )
end

def enqueue
  db = get_db
  db.xquery("INSERT INTO `t` (`created_at`, `executed_at`, `target_id`, `updated_at`) VALUES (?, ?, ?, ?)", Time.now, Time.now, 1, Time.now)
  db.close
end

100000.times do
  enqueue
end
