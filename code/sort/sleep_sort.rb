def sleep_sort(*nums)
  sorted = []

  nums.map do |n|
    Thread.new { sleep n; sorted << n }
  end.map(&:join)

  sorted
end

sleep_sort 3, 1, 4, 2  #=> [1, 2, 3, 4]
