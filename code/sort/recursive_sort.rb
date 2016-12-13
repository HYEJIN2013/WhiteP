def sort arr
  rec_sort arr, []
end

def rec_sort unsorted, sorted
  if unsorted.length <= 0
    return sorted
  end

  # if get to here then more work to do

  smallest = unsorted.pop

  still_unsorted = []

  unsorted.each do |tested_object|
    if tested_object < smallest
      still_unsorted.push smallest
      smallest = tested_object
    else
      still_unsorted.push tested_object
    end
  end
  # now "smallest" really points to the smallest element
  # that "unsorted" contained, and the rest of it is in
  # "still_unsorted"

  sorted.push smallest

  rec_sort still_unsorted, sorted
end

puts(sort(['can', 'feel', 'singing', 'like', 'a', 'can']))
puts
puts ">> the output to your example would be:"
puts(sort(['a','b','c','xxxxx','d','g']))
