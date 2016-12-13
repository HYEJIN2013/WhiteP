data, last_data, offset = [], Array.new(3){""}, Array.new(4){ |index| " " * index * 4;}
RoomPlace.all.each |room| do
  data << room.to_s
end
data.sort.each |place| do
  place.split(', ').each_with_index |part, index| do 
    if (last_data[index] != part || index == 3)
      print offset[index] + "#{last_data[index] = part}\n"
    end
  end
end
