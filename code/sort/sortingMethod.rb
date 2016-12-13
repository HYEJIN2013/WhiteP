def sort_by_length(sort_this_array)
  sort_this_array.sort { |x, y| x.length <=> y.length }
end

def filter(filter_this_array)
  filter_this_array.select { |v| v > 5 }
end
