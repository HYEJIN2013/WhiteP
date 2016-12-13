def sort_list(list)
  new_list = list.split(" ")
  end_list = new_list.pop
  unsorted_list = []
  sorted_list = []

until new_list.length == 1
  new_list.each do |word|
    if word.to_i < end_list.to_i
      unsorted_list.push end_list
      end_list = word
    else
      unsorted_list.push word
    end
  end

sorted_list.push end_list
new_list = unsorted_list
end_list = new_list.pop
unsorted_list = []

end

last_pop = new_list.pop

  if last_pop.to_i > end_list.to_i
    sorted_list.push end_list
    sorted_list.push last_pop
  else
    sorted_list.push last_pop
    sorted_list.push end_list
  end

sorted_list.join(" ")
end
