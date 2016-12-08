lista = ["a"]
listb = ["b", lista]
listc = ["c", listb]
listd = ["d", listc]

data = [ lista, listb, listc, listd, "e" ]

def flat(listdata)
  listdata.inject(Array.new) { |r,e| e.instance_of?(Array) ? r.concat(flat(e)): r << e }
end

p data.flatten
