module BlockSortable
  def encode
    [
      matrix.map(&:last).join,
      matrix.index(self)
    ]
  end

  def matrix
    str = self.dup
    matrix = []
    matrix << str

    (str.length-1).times do
      str = str.left_rotate
      matrix << str
    end

    matrix.sort
  end

  def left_rotate
    str = self.dup
    chars = str.chars
    left = chars.shift
    chars << left
    chars.join
  end

  def last
    self[-1]
  end

end

class String
  prepend BlockSortable
end

puts "payapa".encode
