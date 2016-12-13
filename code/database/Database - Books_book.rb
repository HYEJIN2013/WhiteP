require_relative "module.rb"
require_relative "instance_module.rb"

class Book
  
  extend ClassModule
  include InstanceModule
  
  attr_reader :id
  attr_accessor :name, :genre_id, :location_id, :quantity
  
  # - Initializes a new Book object.
  #
  # - options - HASH containing the various properties to be set as attributes.
  #
  # - id - The Primary Key for a row in the database - INTEGER
  # - name - Name of the book - STRING
  # - genre_id - The Primary Key for the genre the book belongs to - INTEGER
  # - location_id - The Primary Key for the location the book belongs to - INTEGER
  # - quantity - How many books of this name are in a location
  #
  # - Example:
  #
  #      options = {"name" => "The Hobbit", "genre_id" => 1, "location_id" => 1, "quantity" => 3}
  #
  def initialize(options={})
    @id = options["id"]
    @name = options["name"]
    @genre_id = options["genre_id"]
    @location_id = options["location_id"]
    @quantity = options["quantity"]
  end

  # - Updates the assosiated row in the book table with the new values for a book object.
  #
  # - TODO - Needs to return something better
  def save
    CONNECTION.execute("UPDATE books SET name = '#{@name}', genre_id = #{@genre_id}, location_id = #{@location_id}, quantity = #{@quantity} WHERE id = #{id};")
  end
  
  # - Delete's a book from table
  #
  # - TODO - Needs to return something better
  def delete
    CONNECTION.execute("DELETE FROM books WHERE id = #{@id};")
  end
    
    
  # - Checks each attribute to make sure it doesn't equal nil or an empty string
  def valid?
    if @name == nil || @name == ""
      false
    elsif @genre_id == nil
      false
    elsif @location_id == nil
      false
    elsif @quantity == nil
      false
    else
      true
    end
  end

  # - Finds all books assosiated with that location. Creates book objects and inserts them into an array.
  #
  # - location = location_id paramater to search - INTEGER
  #
  # - Returns an array with the book objects that are in that location.
  def self.where_location(location)
    results = CONNECTION.execute("SELECT * FROM books WHERE location_id = #{location}")

    results_as_objects = []
    
    results.each do |result_hash|
      results_as_objects << self.new(result_hash)
    end
    
    return results_as_objects
  end
  
  # - Finds all books assosiated with that genre. Creates book objects and inserts them into an array.
  #
  # - genre = genre_id paramater to search - INTEGER
  #
  # - Returns an array with the book objects that are in that genre.
  def self.where_genre(genre)
    results = CONNECTION.execute("SELECT name FROM books WHERE genre_id = #{genre}")

    results_as_objects = []
    
    results.each do |result_hash|
      results_as_objects << self.new(result_hash)
    end
    
    return results_as_objects
  end
end
