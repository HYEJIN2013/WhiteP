require 'rubygems'
require 'data_mapper'
require 'nokogiri'
# Connect to database
DataMapper.setup(:default, 'mysql://root@localhost/mpuk')

class Event
  include DataMapper::Resource

  property :id,           Serial
  property :etype,        String
  property :uid,          Text   #unique identifier - for forum post/newspost, permalink, for tweet, id, etc.
  property :title,        Text
  property :description,  Text

  property :created_at,   DateTime  #alerted at, put in database at
  property :happened_at,  DateTime  #when the event actually occurred, used for sorting on initial display
end

DataMapper.finalize

events = Event.all(:uid.like => 'insomnia50%', :etype => 'FORUM')
puts "Mapping #{events.size} events"
events.each do |event|
  doc = Nokogiri::HTML.fragment(event.title)
  link = doc.at_css('a')
  link['href'] = "https://forums.multiplay.com/#{event.uid}"
  puts "Updating #{event.uid} to #{link['href']}"
  event.title = doc.to_html
  event.save
end
