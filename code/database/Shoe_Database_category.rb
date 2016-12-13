# Category Class

class Category

  # Assigns an id for identification in instance methods
  #
  # id - Integer assigned as the primary key from the id column
  #
  # Returns the category object created
  def initialize(id)
    @id = id
  end

  # Creates a new category (row) in the categories table
  #
  # category_name - String
  #
  # Returns an empty Array
  def self.add(category_name)
    DATABASE.execute("INSERT INTO categories (name) VALUES ('#{category_name}');")
  end

  # Read method for the categories table
  #
  # Returns all data from the categories table as an Array of Hashes. Each Hash
  #   corresponds with one row of data from the shoes table (one category).
  def self.all
    DATABASE.execute("SELECT * FROM categories;")
  end

  # Reads all shoes in a category object
  #
  # Returns all shoe information in a category from the shoes table as an Array
  #   of Hashes. Each Hash corresponds to a row of data which is stored at the
  #   passed id.
  def shoes
    DATABASE.execute("SELECT * FROM shoes WHERE category_id = #{@id};")
  end

  # Update method for the categories table
  #
  # new_category_name - String
  #
  # Returns an empty Array
  def update(new_category_name)
    DATABASE.execute("UPDATE categories SET name = '#{new_category_name}' WHERE id = #{@id};")
  end

  # Checks to see if the category contains no products.
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
      DATABASE.execute("DELETE FROM categories WHERE id = #{@id};")
    end
  end

end
