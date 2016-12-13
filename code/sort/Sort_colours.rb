#!/usr/bin/env ruby

def sort_colours(str)
  ranking = {
    "blue" => 1,
    "orange" => 2,
    "green" => 3,
    "yellow" => 4,
    "pink" => 5,
    "red" => 6,
    "grey" => 7,
    "lime" => 8
  }

  str.split.sort do |a,b|
    ranking[a] <=> ranking[b]
  end
end

puts sort_colours(%q[orange yellow lime grey pink blue green red])
