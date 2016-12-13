w = (%w[stokrotka katapulta polityka policja pizza watykan kocur osiem])

def words_sorter(words)
  @sorted = Hash.new { |hash, key| hash[key] = [] }

  words.each do |w|
    @sorted[w.length] << w
  end
end

words_sorter(w)

p @sorted
