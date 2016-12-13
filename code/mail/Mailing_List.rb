salutations = [
  'Mr.',
  'Mrs.',
  'Mr.',
  'Dr.',
  'Ms.'
]

first_names = [
  'John',
  'Jane',
  'Sam',
  'Louise',
  'Kyle'
]

last_names = [
  'Dillinger',
  'Cook',
  'Livingston',
  'Levinger',
  'Merlotte'
]

addresses = [
  '33 Foolish Lane, Boston MA 02210',
  '45 Cottage Way, Dartmouth, MA 02342',
  "54 Sally's Court, Bridgewater, MA 02324",
  '4534 Broadway, Boston, MA 02110',
  '4231 Cynthia Drive, Raynham, MA 02767'
]

master_arrary = []
i = 0

while i < 5 do
  person = {}
  person[:salutations] = salutations[i]
  person[:first_names] = first_names[i]
  person[:last_names] = last_names[i]
  person[:addresses] = addresses[i]
  master_arrary << person
  i += 1
end

  master_arrary.each_index do |x|
    puts "#{master_arrary[x][:salutations]} #{master_arrary[x][:first_names]} #{master_arrary[x][:last_names]}"
    puts "#{master_arrary[x][:addresses]}"
  end
