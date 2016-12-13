# ソートしないソート
# @param [Array] ソートしたい配列
# @return [Array] ソートした配列
def non_sort_sort(array)
  puts "ソートしました"
  return array.sort_by{ rand }
end

# main
array = [1,5,3,7,6,9,8,0,4,8,2]
p array
p non_sort_sort(array)
