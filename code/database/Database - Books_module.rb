module ClassModule
  
  require "active_support"
  require "active_support/inflector"
  
  # - Runs a loop for each row in table.
  # - Returns a hash that is split into a readable form.
  def book_table
    puts "ID - NAME - GENRE_ID - LOCATION_ID - QUANTITY"
    self.all.each do |book_hash|
      puts "#{book_hash.id} - #{book_hash.name} - #{book_hash.genre_id} - #{book_hash.location_id} - #{book_hash.quantity}"
    end
  end
  
  # - Returns all columns for every genre in table
  # - Returns a hash that is split into a readable form.
  def genre_table
    puts "ID - Name"
    self.all.each do |genre_hash|
      puts "#{genre_hash.id} - #{genre_hash.name}"
    end
  end
  
  # - Returns all columns for every location in table.
  # - Returns a hash that is split into a readable form.
  def location_table
    puts "ID - Name"
    
    self.all.each do |location_hash|
      puts "#{location_hash.id} - #{location_hash.name}"
    end
  end

  # - Class Method - Gathers all information from the table that is assosiated with the class this is being called on.
  #
  # - Creates new objects for all selected rows and puts them into an array.
  #
  # - Returns the array with objects inside.
  def all
    table_name = self.to_s.pluralize.underscore
    
    results = CONNECTION.execute("SELECT * FROM '#{table_name}';")

    results_as_objects = []
    
    results.each do |result_hash|
      results_as_objects << self.new(result_hash)
    end
    
    return results_as_objects
  end

  # - Retrieves information from a table with the row id == to arguement id
  #
  # - Creates a new object
  #
  # - Returns object
  def find(id)
    table_name = self.to_s.pluralize.underscore
    
    result = CONNECTION.execute("SELECT * FROM '#{table_name}' WHERE id = #{id};")
    result = result.first
    
    self.new(result)
  end
  
  # - Adds a new row into a table with the values taken in the arguement.
  # - Seperates values and keys, puts them into arrays to be put into SQL.
  #
  # - options - Hash
  #
  # - Returns an object
  def add(options={})
    
    table_name = self.to_s.pluralize.underscore
    
    column_names = options.keys
    values = options.values
    
    column_names = column_names.join(", ")
    
    converted_values = []
    
    values.each do |value|
      if value.is_a?(String)
        converted_values << "'#{value}'"
      else
        converted_values << value
      end
    end
    
    converted_values = converted_values.join(", ")
    
    CONNECTION.execute("INSERT INTO #{table_name} (#{column_names}) VALUES (#{converted_values});")
    
    id = CONNECTION.last_insert_row_id
    options["id"] = id
    
    self.new(options)
  end
end
