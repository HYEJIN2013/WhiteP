# Make sure SQLite can be accessed.
require "sqlite3"

# Load/create our database for this program.
CONNECTION = SQLite3::Database.new("backyard.db")

# Make the table.
CONNECTION.execute("CREATE TABLE IF NOT EXISTS backyard (id INTEGER PRIMARY KEY, name TEXT, flower_color TEXT, quantity INTEGER);")
# =>                                                           01,  Daisy,     white

# Get results as an Array of Hashes.
CONNECTION.results_as_hash = true

# ------------------------CRUDs-----------------------------------------


#------------------------ Create ---------------------------------------
#add a complete row
def add_plant(plant_name, flower_color, quantity)
  CONNECTION.execute("INSERT INTO backyard (name, flower_color, quantity) VALUES ('#{plant_name}','#{flower_color}','#{quantity}');")
end

#add a plant name nothing else
def add_plant_name(plant_name)
  CONNECTION.execute("INSERT INTO backyard (name) VALUES ('#{student_name}');")
end

#------------------------ Read -----------------------------------------

#read all rows and columns
def full_backyard
  CONNECTION.execute('SELECT * FROM backyard;')
end

#read specific row by id
def student_name(id)
  result = CONNECTION.execute("SELECT name FROM backyard WHERE id = #{id};")
  result.first["name"]
  # result[0]["name"]
end

#------------------------ Update ---------------------------------------

#change existing plant name with new name using existing id
def change_plant_name(new_plant_name, id)
  CONNECTION.execute("UPDATE backyard SET name = '#{new_plant_name}' WHERE id = #{id};")
end

#change existing plant;s flower color with new color using existing id
def change_plant_name(new_color, id)
  CONNECTION.execute("UPDATE backyard SET flower_color = '#{new_color}' WHERE id = #{id};")
end

#------------------------ Destroy --------------------------------------

#deleting plant row by name
def delete_plant_row(delete_name)
  CONNECTION.execute("DELETE FROM backyard WHERE name = '#{delete_name}';")
end

#_________________________Conversions____________________________________

# This will be integer value, you can convert this int value back to Boolean as follows
Boolean flag2 = (intValue == 1)? true : false;

#_________________________________TESTING________________________________
#empty list of plants array
list_of_plants = []

puts "let's enter some plants into our backyard catalog \n\ What is the plant's name?"
plant_name = gets.chomp.to_s

puts "If that plant has a flower, enter the color, if not just hit enter or type noda."
flower_color = gets.chomp.to_s

puts "How many of these plants are in your backyard?"
quantity = gets.chomp.to_i

add_plant(plant_name, flower_color, quantity)

puts "This will take a while, I've seen your backyard. How's abouts we add all of the 
information at one time. So please type plant name, flower color, and quantity _just a number_."
one_plant_row = gets.chomp

#looping to add the information over and over
begin
#puts one_plant_information into an array by breaking at the comma
one_plant_information = one_plant_row.split(", ")

#takes that array and pushes to a bigger array
list_of_plants.push(one_plant_information)

puts "add another?"
answer = gets.chomp.downcase

#***need to do a loop to continue to do adding
end until answer == "no"

#if person only enters one row of information below works
add_plant(one_plant_information[0], one_plant_information[1], one_plant_information[2],)

puts full_backyard

puts " would you like to delete some? if so enter the name of the plant you wish to delete."
delete_name = gets.chomp

delete_plant_row(delete_name)

puts full_backyard
