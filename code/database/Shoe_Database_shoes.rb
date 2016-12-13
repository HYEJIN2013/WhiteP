# Shoe Class

class Shoe

  # Assigns an id for identification in instance methods
  #
  # id - Integer assigned as the primary key from the id column
  #
  # Returns object created
  def initialize(id)
    @id = id
  end

  # Creates a new shoe (row) in the shoes table
  #
  # shoe_name - String
  # cost - Integer
  # color - String
  # category_id - Integer, foreign key from the categories table
  # location_id - Integer, foreign key from the locations table
  # quantity - Integer, to be added to the location_stock column
  #
  # Returns an empty Array
  def self.add(shoe_name, cost, color, category_id, location_id, quantity)
    DATABASE.execute("INSERT INTO shoes (name, cost, color, category_id, location_id, location_stock) VALUES ('#{shoe_name}', #{cost}, '#{color}', '#{category_id}', '#{location_id}', #{quantity});")
  end

  # Read method for the shoes table
  #
  # Returns all rows from the shoes table as an Array of Hashes. Each Hash is
  #   a row of data.
  def self.all
    DATABASE.execute("SELECT * FROM shoes;")
  end

  # Read method for stock quantities
  #
  # Returns id - Integer, name - String, and location_stock - Integer, from
  #   shoes table as an Array of Hashes. Each Hash corresponds to a row of data.
  def self.quantity
    DATABASE.execute("SELECT id, name, location_stock FROM shoes;")
  end

  # Sums all of the product inventory
  #
  # Returns the sum of all location_stock values - Integer
  def self.total_stock
    DATABASE.execute("SELECT SUM(location_stock) FROM shoes;")
  end

  # Shows all products by cost categories
  #
  # cost_category - String, should be categories of high, medium, or low
  #
  # Returns all row information where the condition is true as an Array of
  #   Hashes. Each Hash corresponds to a row of data in the shoes table that
  #   meets the criteria in the WHERE statement.
  def self.where_cost(cost_category)
    if cost_category == "high"
      DATABASE.execute("SELECT * FROM shoes WHERE cost >= 100;")
    elsif cost_category == "medium"
      DATABASE.execute("SELECT * FROM shoes WHERE cost >= 50 AND cost < 100;")
    else
      DATABASE.execute("SELECT * FROM shoes WHERE cost < 50;")
    end
  end

  # Reads all products with low quantities in location_stock.
  #
  # Returns all row information, for only rows where location_stock is less than
  #   5, as an Array of Hashes. Each Hash corresponds to a row of data in the
  #   shoes table that meets the criteria in the WHERE statement.
  def self.where_quantity_is_low
    DATABASE.execute("SELECT * FROM shoes WHERE location_stock < 5;")
  end

  # Read method for a single shoe product (row) in the shoes table
  #
  # Returns row of information as an Array with a single Hash. The Hash
  #   corresponds to the row of data that matches the given id.
  def information
    DATABASE.execute("SELECT * FROM shoes WHERE id = #{@id};")
  end

  # Update any value for a given field that takes Strings
  #
  # field_name - String
  # new_value - String
  #
  # Returns an empty Array
  def update_strings(field_name, new_value)
    DATABASE.execute("UPDATE shoes SET #{field_name} = '#{new_value}' WHERE id = #{@id};")
  end

  # Update any value for a given field that takes Integers
  #
  # field_name - String
  # new_value - Integer
  #
  # Returns an empty Array
  def update_integers(field_name, new_value)
    DATABASE.execute("UPDATE shoes SET #{field_name} = #{new_value} WHERE id = #{@id};")
  end

  # Updates the name value in the shoes table
  #
  # new_name - String
  #
  # Returns an empty Array
  def update_name(new_name)
    update_strings("name", new_name)
  end

  # Updates the cost value in the shoes table
  #
  # new_cost - Integer
  #
  # Returns an empty Array
  def update_cost(new_cost)
    update_integers("cost", new_cost)
  end

  # Updates the color value in the shoes table
  #
  # new_color - String
  #
  # Returns an empty Array
  def update_color(new_color)
    update_strings("color", new_color)
  end

  # Assigns/updates the location_id of a shoe instance
  #
  # new_location_id - Integer
  #
  # Returns an empty Array
  def update_location(new_location_id)
    update_integers("location_id", new_location_id)
  end

  # Updates the quantity of a product for a given id
  #
  # to_add - Integer
  #
  # Returns an empty Array
  def update_quantity(to_add)
    current_quantity = DATABASE.execute("SELECT location_stock FROM shoes WHERE id = #{@id};").first['location_stock']
    DATABASE.execute("UPDATE shoes SET location_stock = #{current_quantity + to_add} WHERE id = #{@id};")
  end

  # Assigns/updates the category_id of a shoe instance
  #
  # new_category_id - Integer
  #
  # Returns an empty Array
  def update_category(new_category_id)
    update_integers("category_id", new_category_id)
  end

  # Deletes a shoe row from the shoes table
  #
  # Returns an empty Array
  def delete
    DATABASE.execute("DELETE FROM shoes WHERE id = #{@id};")
  end

end
