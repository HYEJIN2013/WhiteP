class GitDatabase 
  attr_accessor :items
  def initialize
    `git init`
    @items = {}
  end
 
  def save(key, input)
    set(key, hash_object(input.to_s))
  end

  def find(key)
    cat_file(@items[key])
  end

  def set(key, hash)
    @items[key] = hash
  end

  def hash_object(string)
    `echo #{string} | git hash-object -w --stdin`.strip!
  end

  def cat_file(hash)
    `git cat-file -p #{hash}`
  end
end

def test
  a = GitDatabase.new
  a.save("Eggs", 12)
  a.save(10420, 13)
  a.save(:symstuff, 14)
  a.save(0.1, 132)
  puts a.find(0.1)
  puts a.find(:symstuff)
  puts a.find(10420)
  puts a.find("Eggs")
end

test
# => 132
# 14
# 13
# 12
