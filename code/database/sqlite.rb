# 1. Require the gem sqlite3.  You must `gem install sqlite3` if you get an error
# stating `cannot load such file -- sqlite3`
# This will add the gem to your local gemset
require 'sqlite3'
# Faker makes fake data.  Same deal on the gem
require 'faker'

# 2. Simply running the command on line 9 creates a database in
# your working directory

# 3. Set up a connection to the database you have created
sqlite3 = SQLite3::Database.new 'sqlite.db'


# 4. Ruby your SQL commands in ruby

# Drop the table if it exist so we can run create table over and over
sqlite3.execute( "drop table students" )
# Create a table: Students
sqlite3.execute( "
create table students
(
lastname  varchar(255),
firstname varchar(255),
cohort    varchar(255),
phase     int
);
  ")

# 5 Insert some data into your database
sqlite3.execute( "
insert into students values ('Lubaway', 'Topher', 'Fence Lizard', 14);
  ")
10.times do
sqlite3.execute( "
insert into students values ('#{Faker::Name.last_name}', '#{Faker::Name.first_name}', '#{Faker::Company.bs}', rand(4));
  ")
end
