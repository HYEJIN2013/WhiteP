#!/usr/local/bin/ruby
require 'sinatra'
require 'nokogiri'

XMLFILEPATH = 'database.xml'

# Put the XML database
get '/' do
  [200, {"Content-Type" => 'text/xml'}, File.open(XMLFILEPATH, 'r')]
end

# Accept data on the 'data' parameter, and drop it into /posts
#
#   POST / HTTP/1.0
#  
#   data[name]=Alex Bartlow&data[dob]=06061987
post '/' do
  fr = File.open(XMLFILEPATH, 'r')
  
  doc = Nokogiri::XML::Document.parse(fr)
  fr.close
  
  data_node = Nokogiri::XML::Node.new("data")
  params[:data].each do |key, value|
    attribute_node = Nokogiri::XML::Node.new(key)
    attribute_node.content = value
    data_node.add_child attribute_node
  end
  
  doc.xpath('/posts')[0].add_child(data_node)
  
  File.open(XMLFILEPATH, 'w') do |fw|
    fw.write doc.to_xml
  end
  [200, {}, [""]]
end
