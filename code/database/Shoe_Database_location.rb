# Location Class

class Location

  # Assigns an id for identification in instance methods
  #
  # id - Integer assigned as the primary key from the id column
  #
  # Returns location object created
  def initialize(id)
    @id = id
  end

  # Creates a new location (row) in the locations table
  #
  # location_name - String
  #
  # Returns an empty Array
  def self.add(location_name)
    DATABASE.execute("INSERT INTO locations (name) VALUES ('#{location_name}');")
  end

  # Read method for the locations table
  #
  # Returns all information from the locations table as an Array of Hashes. Each
  #   Hash corresponds to one row of data (one location).
  def self.all
    DATABASE.execute("SELECT * FROM locations;")
  end

  # Reads all shoes at a location object
  #
  # Returns all shoe information at one location from the shoes table as an
  #  Array of Hashes. Each Hash corresponds to a row of data which is stored at #  the passed id.
  def shoes
    DATABASE.execute("SELECT * FROM shoes WHERE location_id = #{@id};")
  end

  # Update method for the locations table
  #
  # new_location_name - String
  #
  # Returns an empty Array
  def update(new_location_name)
    DATABASE.execute("UPDATE locations SET name = '#{new_location_name}' WHERE id = #{@id};")
  end

  # Checks to see if the location contains no products.
  #
  # Returns true or false - Binary
  def empty?
    self.shoes == []
  end

  # Delete a category from the categories table
  #
  # Returns an empty Array
  def delete
    if self.empty?
      DATABASE.execute("DELETE FROM locations WHERE id = #{@id};")
    end
  end

end
