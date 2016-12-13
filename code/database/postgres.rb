# 1. Require the gem PG.  You must `gem install pg` if you get an error
# stating `cannot load such file -- pg`
# This will add the gem to your local gemset
require 'pg'
# Faker makes fake data.  Same deal on the gem
require 'faker'

# 2. From the command line `createdb YOUR_DATABASE_NAME`

# 3. Set up a connection to the database you have created
pg_connection = PG.connect( dbname: 'YOUR_DATABASE_NAME' )


# 4. Ruby your SQL commands in ruby

# Drop the table if it exist so we can run create table over and over
pg_connection.exec( "drop table students" )

# Create a table: Students
pg_connection.exec( "
  create table students
  (
    lastname  varchar(255),
    firstname varchar(255),
    cohort    varchar(255),
    phase     int
  );
")
10.times do
pg_connection.exec( "
insert into students values ('#{Faker::Name.last_name}', '#{Faker::Name.first_name}', '#{Faker::Company.bs}', #{rand(4)});
  ")
end
