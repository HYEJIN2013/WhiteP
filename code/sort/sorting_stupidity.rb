# encoding: utf-8

# denne sorteringen kommer fra databasen – legg merke til at å kommer før ø
alphabet = {:a=>"A", :b=>"B", :c=>"C", :d=>"D", :e=>"E", :f=>"F", :g=>"G", :h=>"H", :i=>"I", :j=>"J", :k=>"K", :l=>"L", :m=>"M", :n=>"N", :o=>"O", :p=>"P", :r=>"R", :s=>"S", :t=>"T", :u=>"U", :v=>"V", :w=>"W", :z=>"Z", :aa=>"Å", :oe=>"Ø"}

sorted_alphabet = {}
sorting = ('a'..'z').to_a + %w(ae oe aa)

sorting.each do |letter|
  if alphabet.has_key?(letter.to_sym)
    sorted_alphabet[letter.to_sym] = alphabet[letter.to_sym]
  end
end

puts sorted_alphabet

# => {:a=>"A", :b=>"B", :c=>"C", :d=>"D", :e=>"E", :f=>"F", :g=>"G", :h=>"H", :i=>"I", :j=>"J", :k=>"K", :l=>"L", :m=>"M", :n=>"N", :o=>"O", :p=>"P", :r=>"R", :s=>"S", :t=>"T", :u=>"U", :v=>"V", :w=>"W", :z=>"Z", :oe=>"Ø", :aa=>"Å"}
