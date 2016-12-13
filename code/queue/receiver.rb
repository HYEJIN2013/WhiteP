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

def dequeue
  db = get_db

  queues = db.query("select * from t where status = 0 and executed_at < now()")
  queues.each do |q|
    db.xquery("update t set status = 1 where id = ? and status = 0", q["id"])
    if db.affected_rows() == 1
      puts q["id"]
      db.xquery("delete from t where id = ?", q['id'])
    end
  end
  db.close
end

10000.times do
  dequeue
end
