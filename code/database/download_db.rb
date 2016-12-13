#!/usr/bin/env ruby
#
# Wubin Qu <quwubin@gmail.com>

require 'rubygems'
require 'thor'
require_relative 'biodb'

class Download < Thor

  desc "list", "list available databases"
  def list
    db = Biodb::Ncbi.new
    puts db.list
  end

  desc "download" ,"download databases you specificied"
  method_option :database,  :default => nil, :aliases => "-d",
  :desc => "database name to be downloaded", :required => true,
  :type => :array
  def download
    db = Biodb::Ncbi.new
    database = options[:database]
    db.download(database)
  end
end

Download.start
