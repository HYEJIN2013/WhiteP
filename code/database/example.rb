require 'sqlite3'
require 'faker'

$db = SQLite3::Database.new "ecommerce.db"

module EcommerceDB
  def self.setup
    $db.execute_batch(
      <<-SQL
CREATE TABLE users (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name VARCHAR(64) NOT NULL,
email VARCHAR(100) UNIQUE NOT NULL,
photo_id INTEGER,
created_at DATETIME NOT NULL,
updated_at DATETIME NOT NULL,
FOREIGN KEY(photo_id) REFERENCES photos(id)
);
CREATE TABLE photos (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name VARCHAR(64) NOT NULL,
url VARCHAR(200) NOT NULL,
created_at DATETIME NOT NULL,
updated_at DATETIME NOT NULL
);
CREATE TABLE products (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name VARCHAR(64) NOT NULL,
description TEXT(64) NULL,
user_id INTEGER,
photo_id INTEGER,
created_at DATETIME NOT NULL,
updated_at DATETIME NOT NULL,
FOREIGN KEY(user_id) REFERENCES users(id),
FOREIGN KEY(photo_id) REFERENCES photos(id)
);
      SQL
    )
  end

  def self.seed
    $db.execute_batch(
      <<-SQL
        INSERT INTO users
          (name, email, photo_id, created_at, updated_at)
        VALUES
          ('#{Faker::Name.name}', '#{Faker::Internet.email}', 1, DATETIME('now'), DATETIME('now')),
          ('#{Faker::Name.name}', '#{Faker::Internet.email}', 2, DATETIME('now'), DATETIME('now')),
          ('#{Faker::Name.name}', '#{Faker::Internet.email}', 3, DATETIME('now'), DATETIME('now')),
          ('#{Faker::Name.name}', '#{Faker::Internet.email}', 4, DATETIME('now'), DATETIME('now')),
          ('#{Faker::Name.name}', '#{Faker::Internet.email}', 5, DATETIME('now'), DATETIME('now'));
# only put non-key values and 
             INSERT INTO photos
           (name, url, created_at, updated_at)
        VALUES
          ('#{Faker::Commerce.product_name}', '#{Faker::Lorem.sentence}', '#{(1..100).to_a.sample}', 1, DATETIME('now'), DATETIME('now')),
          ('#{Faker::Commerce.product_name}', '#{Faker::Lorem.sentence}', '#{(1..100).to_a.sample}', 2, DATETIME('now'), DATETIME('now')),
          ('#{Faker::Commerce.product_name}', '#{Faker::Lorem.sentence}', '#{(1..100).to_a.sample}', 3, DATETIME('now'), DATETIME('now')),
          ('#{Faker::Commerce.product_name}', '#{Faker::Lorem.sentence}', '#{(1..100).to_a.sample}', 4, DATETIME('now'), DATETIME('now')),
          ('#{Faker::Commerce.product_name}', '#{Faker::Lorem.sentence}', '#{(1..100).to_a.sample}', 5, DATETIME('now'), DATETIME('now'));
         INSERT INTO products
           (name, description, created_at, updated_at)
         VALUES
          ('#{Faker::Commerce.product_name}', '#{Faker::Internet.url}', DATETIME('now'), DATETIME('now')),
          ('#{Faker::Commerce.product_name}', '#{Faker::Internet.url}', DATETIME('now'), DATETIME('now')),
          ('#{Faker::Commerce.product_name}', '#{Faker::Internet.url}', DATETIME('now'), DATETIME('now')),
          ('#{Faker::Commerce.product_name}', '#{Faker::Internet.url}', DATETIME('now'), DATETIME('now')),
          ('#{Faker::Commerce.product_name}', '#{Faker::Internet.url}', DATETIME('now'), DATETIME('now'));
      SQL
    )
  end

end


EcommerceDB.setup
EcommerceDB.seed
