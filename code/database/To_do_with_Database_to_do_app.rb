require 'pg'
require './lib/to_do'
require './lib/list'
require 'pry'

DB = PG.connect(:dbname => 'to_do_test')

def init
  puts "\n\nHello non-programmer! you know it took me all day to write this!\n\n\n"
  puts "Please enter 'L' to make a new list"
  puts "Please enter 'T' to make a new task"
  puts "Please enter 'D' to delete a task or list"
  puts "Please enter 'P' to print lists with tasks"
  puts "Please enter 'X' to exit\n\n"
  user_choice = gets.chomp.downcase

  if user_choice == 'l'
    add_list
    init
  elsif user_choice == 't'
    add_task
    init
  elsif user_choice == 'd'
    delete
    init
  elsif user_choice == 'p'
    print
    init
  elsif user_choice == 'x'
    exit  
  else 
    puts "\n\nEnter a valid input!\n\n"
    init        
  end  
end

def add_list
  puts "\n\nEnter list name:\n"
  user_choice = gets.chomp
  List.new(user_choice).save
  puts "\n\n List #{user_choice} saved.  You welcome\n\n"
end

def add_task
  puts "\n\nEnter task description:\n"
  user_description = gets.chomp
  print_list
  puts "\n\nEnter list to store task in:\n"
  user_list = gets.to_i
  Task.new(user_description, user_list).save
  puts "\n\n Task #{user_description} saved.  You welcome\n\n"
end

def print_list
  List.all.each  do |list|
    # binding.pry
    puts "List # #{list.id} List name: #{list.name}"
  end
end    

init  
