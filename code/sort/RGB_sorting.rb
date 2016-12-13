#!/usr/bin/env ruby

t = [:r, :g, :b]
puts (inp = ARGV[0].split("").map {|x| x.downcase.to_sym}).inspect
cc = Hash[t.map {|c| [c,inp.count(c)]}]
expec = t.map {|c| [c]*cc[c]}.flatten
puts (slc = Hash[t.zip([(0...cc[:r]), (cc[:r]...cc[:r]+cc[:g]), (cc[:r]+cc[:g]...cc[:r]+cc[:g]+cc[:b])])]).inspect
inp.each_with_index do |c, i|
	next if expec[i] == c #ok
	if inp[slc[c]].index(expec[i]) then # fix 2 positions
		swap = inp[slc[c]].index(expec[i]) + slc[c].min
	else #fix 1 position
		swap = inp[slc[(t-[c]-[expec[i]])[0]]].index(expec[i]) + slc[(t-[c]-[expec[i]])[0]].min
	end
		inp[swap] = c; inp[i] = expec[i];
		puts "swap #{i} & #{swap}"
	puts inp.inspect
end
