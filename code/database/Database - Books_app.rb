require "sqlite3"
require_relative "book.rb"
require_relative "genre.rb"
require_relative "location.rb"
require_relative "module.rb"
require_relative "instance_module.rb"

CONNECTION = SQLite3::Database.new("inventory.db")

CONNECTION.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, name TEXT NOT NULL, genre_id INTEGER NOT NULL, location_id INTEGER NOT NULL, quantity INTEGER NOT NULL, FOREIGN KEY(location_id) REFERENCES locations(id), FOREIGN KEY(genre_id) REFERENCES genres(id));")
CONNECTION.execute("CREATE TABLE IF NOT EXISTS genres (id INTEGER PRIMARY KEY, name TEXT NOT NULL);")
CONNECTION.execute("CREATE TABLE IF NOT EXISTS locations (id INTEGER PRIMARY KEY, name TEXT NOT NULL);")

# Get results as an Array of Hashes.
CONNECTION.results_as_hash = true

# ------------------------------------------------------------

continue = "y"

while continue != "n"
  puts "Hello! What would you like to work with today?"
  puts "Books? (1)"
  puts "Genres? (2)"
  puts "Locations? (3)"
  puts "Search? (4)"

  table_answer = gets.chomp.to_i

  # - Start of Books
  if table_answer == 1
    puts "What would you like to do with Books?"
    puts "Add a book? (1)"
    puts "Edit a book? (2)"
    puts "View book information? (3)"
    puts "Delete a book? (4)"
  
    book_answer = gets.chomp.to_i
  
    # - Add a book
    if book_answer == 1
      puts "What is the name of the book?"
      book_name = gets.chomp
    
      puts "What genre is the book?"
      Genre.genre_table
      book_genre = gets.chomp
      while book_genre.empty?
        puts "Sorry, please enter a genre"
        book_genre = gets.chomp
      end
        book_genre.to_i
    
      puts "Where is the book?"
      Location.location_table
      book_location = gets.chomp
      while book_location.empty?
        puts "Sorry, please enter a location"
        book_location = gets.chomp
      end
      book_location.to_i
      
      puts "How many are there?"
      book_quantity = gets.chomp
      while book_quantity.empty?
        puts "Sorry, please enter a quantity"
        book_quantity = gets.chomp
      end
        book_quantity.to_i
      
      book_object = Book.new({"name" => book_name, "genre_id" => book_genre, "location_id" => book_location, "quantity" => book_quantity})
      
      if book_object.valid?
        Book.add({"name" => book_name, "genre_id" => book_genre, "location_id" => book_location, "quantity" => book_quantity})
      else
        puts "Sorry, wasn't able to add to database at this time."
      end
    end
    
    # - Edit a book
    if book_answer == 2
      puts "What book would you like to edit?"
      Book.book_table
      book_id = gets.chomp.to_i
      
      book_object = Book.find(book_id)
      
      puts "What would you like to edit?"
      puts "Book name? (1)"
      puts "Book genre? (2)"
      puts "Book location? (3)"
      puts "Book quantity? (4)"
      
      book_edit = gets.chomp.to_i
      
      # - Edit Book name
      if book_edit == 1
        puts "What is the new book name?"
        book_object.name = gets.chomp.to_s
        book_object.save
      end
      
      # - Edit Book genre
      if book_edit == 2
        puts "What is the new book genre?"
        Genre.genre_table
        book_object.genre_id = gets.chomp.to_i
        book_object.save
      end
      
      # - Edit Book location
      if book_edit == 3
        puts "What is the new book location?"
        Location.location_table
        book_object.location_id = gets.chomp.to_i
        book_object.save
      end
      
      # - Edit Book quantity
      if book_edit == 4
        puts "What is the new quantity?"
        book_object.quantity = gets.chomp.to_i
        book_object.save
      end
    end
    
    # - View book information
    if book_answer == 3
      puts "What book would you like to view?"
      Book.book_table
      book_id = gets.chomp.to_i
      
      this_book = Book.find(book_id)
      
      puts "#{this_book.id} - #{this_book.name} - #{this_book.genre_id} - #{this_book.location_id} - #{this_book.quantity}"
    end
    
    # - Delete Book
    if book_answer == 4
      puts "What book would you like to delete?"
      Book.book_table
      book_id = gets.chomp.to_i
      
      this_book = Book.find(book_id)
      
      this_book.delete
    end
  end
  
  # - Start of genres
  
  if table_answer == 2
    puts "What would you like to do with genres?"
    puts "Add a genre? (1)"
    puts "Delete a genre? (2)"
    
    genre_answer = gets.chomp.to_i
    
    # - Add a genre
    if genre_answer == 1
      puts "What is the genre name?"
      genre_name = gets.chomp
      
      genre_object = Genre.new({"name" => genre_name})
      if genre_object.valid?
        Genre.add({"name" => genre_name})
      else
        puts "Sorry, we weren't able to add that genre at this time."
      end
    end
    
    # - Delete a genre
    if genre_answer == 2
      puts "Which genre would you like to delete?"
      Genre.genre_table
      genre_id = gets.chomp.to_i
      
      genre_object = Genre.find(genre_id)
      
      # - Checks to see if genre is empty before deleting.
      if genre_object.delete_category("genre") == false
        puts "Sorry, that genre contains books. You may only delete an empty genre."
      end
    end
  end
  
  # - Start location
  if table_answer == 3
    puts "What would you like to do with locations?"
    puts "Add a location? (1)"
    puts "Delete a location? (2)"
    
    location_answer = gets.chomp.to_i
    
    # - Add location
    if location_answer == 1
      puts "What is the location name?"
      location_name = gets.chomp
      
      location_object = Location.new({"name" => location_name})
      if location_object.valid?
        Location.add({"name" => location_name})
      else
        puts "Sorry, we weren't able to add that genre at this time."
      end
    end
    
    # - Delete location
    if location_answer == 2
      puts "Which location would you like to delete?"
      Location.location_table
      location_id = gets.chomp.to_i
      
      location_object = Location.find(location_id)
      
      # - Checks to see if any books have that location. If true, delete. If false, return that can't delete.
      if location_object.delete_category("location") == false
        puts "Sorry, that location contains books. You may only delete an empty genre."
      end
    end
  end
  
  # - Start search
  if table_answer == 4
    puts "Search for Book by:"
    puts "Location (1)"
    puts "Genre (2)"
    search_answer = gets.chomp.to_i
    
    # - Search by location
    if search_answer == 1
      puts "Which location?"
      Location.location_table
      location = gets.chomp
      
      Book.where_location(location).each do |object|
        puts "#{object.name}"
      end
    end
    
    # - Search by genre
    if search_answer == 2
      puts "Which genre?"
      Genre.genre_table
      genre = gets.chomp
      
      Book.where_genre(genre).each do |object|
        puts "#{object.name}"
      end
    end
  end
    
  puts "Would you like to do something else? (Y/N)"
  continue = gets.chomp
end
