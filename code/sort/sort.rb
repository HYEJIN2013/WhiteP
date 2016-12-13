# Sort the array from lowest to highest
def bubblesort(arr)
 n = arr.length
  loop do
    swapped = false 
    (n-1).times do |i| 
     if arr[i-1] > arr[i]
      then arr[i-1], arr[i] =  arr[i], arr[i-1]
      swapped = true
     end
    end 
    break if not swapped 
  end

  arr
end

# # Find the maximum 
# def maximum(arr)
#   sort(arr).last
# end

# def minimum(arr)
#   sort(arr).first
# end
 
# expect it to return 42 below
result = bubblesort([2, 42, 22, 02]).last
puts "max of 2, 42, 22, 02 is: #{result}"

# expect it to return 2 below
result = bubblesort([2, 42, 22, 02]).first
puts "min of 2, 42, 22, 02 is: #{result}"

 
# expect it to return nil when empty array is passed in
result = bubblesort([])
puts "max on empty set is: #{result.inspect}"
result = bubblesort([])
puts "min on empty set is: #{result.inspect}"
 
result = bubblesort([-23, 0, -3]).last            
puts "max of -23, 0, -3 is: #{result}"
 
result = bubblesort([6]).last
puts "max of just 6 is: #{result}"
