########################
# NYC PIGEON ORGANIZER #
########################
require 'pry'
# Start with the following collected data on NYC pigeons.

pigeon_data = {
  :color => {
    :purple => ["Theo", "Peter Jr.", "Lucky"],
    :grey => ["Theo", "Peter Jr.", "Ms .K"],
    :white => ["Queenie", "Andrew", "Ms .K", "Alex"],
    :brown => ["Queenie", "Alex"]
  },
  :gender => {
    :male => ["Alex", "Theo", "Peter Jr.", "Andrew", "Lucky"],
    :female => ["Queenie", "Ms .K"]
  },
  :lives => {
    "Subway" => ["Theo", "Queenie"],
    "Central Park" => ["Alex", "Ms .K", "Lucky"],
    "Library" => ["Peter Jr."],
    "City Hall" => ["Andrew"]
  }
}

def pigeon_sort(hash)
  pigeon_data = {}

  hash.each do |characteristics, options|
    options.each do |option, names_list|
      names_list.each do |bird_name|
        pigeon_data[bird_name] ||= {} 
        case characteristics
        when :color
          pigeon_data[bird_name][:color] ||= []
          pigeon_data[bird_name][:color] << option
        when :gender
          pigeon_data[bird_name][:gender] ||= {}
          pigeon_data[bird_name][:gender] = option
        when :lives
          pigeon_data[bird_name][:lives] ||= {}
          pigeon_data[bird_name][:lives] = option
        end
      end
    end
  end
  pigeon_data
end

binding.pry
# want to create an each method for the main attributes (color, gender, lives)
#   use the k, v pair to access the options for the main attributes
# create another each method to sort through the keys and access the values 
# create a hash if one doesn't already exist for that bird, otherwise add them to that hash

# use if/else statement to filter respective attribute data into the correct k-v pairs


# Iterate over the hash above collecting each pigeon by name and insert it
# as the key of a new hash where each name holds the attributes for that bird. 
# Your output should match the hash below:

# pigeon_list = {
#   "Theo" => {
#     :color => ["purple", "grey"],
#     :gender => "male",
#     :lives => "Subway"
#   },
#   "Peter Jr." => {
#     :color => ["purple", "grey"],
#     :gender => "male",
#     :lives => "Library"
#   },
#   "Lucky" => {
#     :color => ["purple"],
#     :gender => "male",
#     :lives => "City Hall"
#   },
#   "Ms .K" => {
#     :color => ["grey", "white"],
#     :gender => "female",
#     :lives => "Central Park"
#   },
#   "Queenie" => {
#     :color => ["white", "brown"],
#     :gender => "female",
#     :lives => "Subway"
#   },
#   "Andrew" => {
#     :color => ["white"],
#     :gender => "male",
#     :lives => "Central Park"
#   },
#   "Alex" => {
#     :color => ["white", "brown"],
#     :gender => "male",
#     :lives => "Central Park"
#   }
# }
