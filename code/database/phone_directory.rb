number_check_regex = /\A\d{3}.\d{3}.\d{4}\z/

phone_numbers = {
  "Dan" => {
    home: "508.555.5555",
    mobile: "617.555.1234",
    pager: ""
  },
  "Sam" => {
    home: "508.123.4567",
    mobile: "617.849.1724",
    pager: "508.222.2222"
  },
  "Adoun" => {
    home: "617.456.7890",
    mobile: "508.787.8430",
    pager: ""
  },
  "Jane" => {
    home: "",
    mobile: "508.555.3333",
    pager: ""
  },
  "Tony" => {
    home: "508.444.4444",
    mobile: "508.333.3333",
    pager: ""
  }
}

phone_numbers.each do |a,b|
  if number_check_regex =~ b[:home]
    puts "#{a}'s Home phone number is #{b[:home]}"
  end
  if number_check_regex =~ b[:mobile]
    puts "#{a}'s Mobile phone number is #{b[:mobile]}"
  end
  if number_check_regex =~ b[:pager]
    puts "#{a}'s Pager number is #{b[:pager]}"
  end
end
