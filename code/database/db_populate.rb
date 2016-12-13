require "sqlite3"

db = SQLite3::Database.open "test.db"
db.execute "INSERT INTO posts (title) VALUES('unigoats');"

# last_row_id = db.last_insert_row_id
# puts last_row_id

select_statement = db.prepare "SELECT * FROM posts;"
results = select_statement.execute
puts results.class

results.each do |row|
  puts row
end

results.close if results
db.close if db
