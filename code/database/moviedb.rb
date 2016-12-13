favorite_movies = [
  { title: 'The Big Lebowski', year_released: 1998, director: 'Joel Coen', imdb_rating: 8.2 },
  { title: 'The Shining', year_released: 1980, director: 'Stanley Kubrick', imdb_rating: 8.5 },
  { title: 'Troll 2', year_released: 1990, directory: 'Claudio Fragasso', imdb_rating: 2.5 }
]


favorite_movies.each do |movie|
  puts "#{movie[:year_released]}: #{movie[:title]}"
end
