require 'sqlite3'
require 'faker'

$db =SQLite3::Database.new( "test.db" )

$db.execute <<-SQL
  create table dummy (
    id INTEGER PRIMARY KEY,
    first_name varchar(30),
    last_name varchar(30),
    email VARCHAR,
    phone VARCHAR,
    created_at datetime DEFAULT CURRENT_TIMESTAMP,
    updated_at datetime DEFAULT CURRENT_TIMESTAMP
  );
SQL

1000.times do
$db.execute("INSERT INTO dummy ('first_name', 'last_name', 'email', 'phone')
            VALUES (?, ?, ?, ?)", [Faker::Name.first_name, Faker::Name.last_name, Faker::Internet.email,Faker::PhoneNumber.phone_number, ])
end
