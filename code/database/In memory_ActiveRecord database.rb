ActiveRecord::Base.establish_connection(:adapter => 'sqlite3', :database => ':memory:') # in memory database

ActiveRecord::Schema.define do
  # migrations
end

# models
