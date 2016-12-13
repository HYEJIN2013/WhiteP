blocks = (0..8).to_a.shuffle
puts blocks.inspect

i = 0
while i < 8
  until i == blocks[i]
    j = blocks[i]
    #swap blocks[i] with blocks[blocks[i]]
    blocks[i], blocks[j] = blocks[j], blocks[i]
  end
  i += 1
end

puts blocks.inspect
