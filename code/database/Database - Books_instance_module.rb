module InstanceModule
  
  require "active_support"
  require "active_support/inflector"
  
  # - First sets x to equal the array returned containing hashes of objects that have that location
  # - Checks to see if that returned array is empty. If empty - True, else False
  # - Delete's the location if x == True and returns an empty array. Returns false if x == False.
  def delete_category(class_name)
    table_name = class_name.pluralize
    table_id = class_name + "_id"
    
    x = CONNECTION.execute("SELECT * FROM books WHERE #{table_id} = #{@id};")
    if x == []
      CONNECTION.execute("DELETE FROM '#{table_name}' WHERE id = #{@id};")
    else
      false
    end
  end
end
