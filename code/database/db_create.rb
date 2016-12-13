require "sqlite3"

db = SQLite3::Database.new "test.db"
db.execute "CREATE TABLE posts
  (id INTEGER PRIMARY KEY, title TEXT NOT NULL);"

db.close if db
