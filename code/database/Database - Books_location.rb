require_relative "module.rb"
require_relative "instance_module.rb"

class Location
  
  extend ClassModule
  include InstanceModule
  
  attr_reader :id
  attr_accessor :name
  
  # - Initializes a new location object. Takes its arguements in a hash. 
  #
  # - Example:
  #       options = {"name" = "Iowa"}
  def initialize(options={})
    @id = options["id"]
    @name = options["name"]
  end
 
  # - Updates the assosiated row in the book table with the new values for a book object.
  #
  # - TODO - Needs to return something better
  def save
    CONNECTION.execute("UPDATE locations SET name = '#{@name}' WHERE id = #{id};")
  end
  
  # - Checks to make sure location name is not nil or an empty string.
  #
  # - Returns T/F
  def valid?
    if @name == nil || @name == ""
      false
    else
      true
    end
  end

end
