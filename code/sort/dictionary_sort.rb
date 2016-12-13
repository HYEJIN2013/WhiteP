puts "Type a word:"
  list = []
  word = ""

  until (word = gets.chomp).empty? do
    list << word
    puts "Type another word (or press enter to finish):"
  end

  size = list.count
  puts "Congratulations! Your dictionary has #{size} words:"
  puts list.sort_by { |x| x.downcase }
