require 'sqlite3'

FIRST_DB = SQLite3::Database.new("database.db")

FIRST_DB.execute('CREATE TABLE IF NOT EXISTS account (id INTEGER PRIMARY KEY,name TEXT, transaction_amount INTEGER);')

FIRST_DB.results_as_hash = true

def add_trans(trans_name, amount)
  FIRST_DB.execute("INSERT INTO account (name, transaction_amount) VALUE ('#{trans_name}', #{amount});")
end

def change_trans_name(new_trans_name, id)
  FIRST_DB.execute("UPDATE account SET name = '#{new_trans_name}' WHERE id = #{id};")
end

def check_account
  FIRST_DB.execute('SELECT * FROM account;')
end

def get_trans_name(id)
  name = FIRST_DB.execute("SELECT name FROM account WHERE id = #{id};")
  name.first("name")
end
