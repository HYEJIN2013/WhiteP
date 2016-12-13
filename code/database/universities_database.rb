require 'pry'
require 'pg' # this is our database gem

# this establishes a connection to the database
conn = PG.connect(dbname: 'ga-class', host: 'localhost')

puts "name?"
name = gets.chomp
puts "address?"
address = gets.chomp
puts "undergrads?"
undergrads = gets.chomp
puts "grads?"
grads = gets.chomp
puts "founded?"
founded = gets.chomp

# this executes a SQL statement, using Ruby string interpolation
conn.exec("INSERT INTO universities (name, address, undergrads, grads, founded) VALUES ('#{name}', '#{address}', '#{undergrads}', '#{grads}', '#{founded}')")

# this executes a SQL statement to query the database for all students
result = conn.exec("SELECT * FROM universities")
result.each do |school|
  puts school
end
binding.pry

conn.exec("DELETE FROM universities WHERE id = '#{14}'")
