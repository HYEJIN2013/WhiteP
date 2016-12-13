require 'sqlite3'

$db = SQLite3::Database.new "<database_name.db>"

module StudentDB
  # pry
  def self.setup
    $db.execute_batch(
      <<-SQL
        CREATE TABLE students (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          first_name VARCHAR(64) NOT NULL,
          last_name VARCHAR(64) NOT NULL,
          gender ENUM NOT NULL,
          birthday DATE NOT NULL,
          email VARCHAR (60) NOT NULL,
          phone VARCHAR (30) NOT NULL,
          created_at DATETIME NOT NULL,
          updated_at DATETIME NOT NULL
        );
      SQL
    )
  end

  def self.seed
    # Add a few records to your database when you start
    $db.execute(
      <<-SQL
        INSERT INTO students
          (first_name, last_name, gender, birthday, email, phone, created_at, updated_at)
        VALUES
        
        
          ('Brick','Thornton', 'M', '1981-03-12', 'brick@exampleemail.com', '1-555-555-5555', DATETIME('now'), DATETIME('now')),
          ('Caroline','Artz', 'F', '1984-01-03', 'caroline@exampleemail.com', '1-555-566-5666', DATETIME('now'), DATETIME('now')),
          ('Jason','Chodera', 'M', '1977-10-14', 'jason@exampleemail.com', '1-555-775-5885',DATETIME('now'), DATETIME('now'));
      SQL
    )
  end
end
