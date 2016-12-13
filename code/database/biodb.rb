#!/usr/bin/env ruby
#
# Wubin Qu <quwubin@gmail.com>

require 'fileutils'
module Biodb 
  module DbProcess
    attr_reader :ftp_address, :dir
    attr_accessor :available_dbs

    def set_up(ftp_address, dir)
      @ftp_address = ftp_address
      @dir = dir
    end

    def list
      file_list = '.' + @dir.gsub(/\//, "_") + '.list'

      if not File.exists?(file_list) or (Time.now - File.ctime(file_list)) / 3600 / 24 > 7
	files = `lftp #{@ftp_address} -e "cd #{@dir}; ls; exit"`
	File.open(file_list, 'w') do |ff|
	  ff.puts(files)
	end
      end

      files = File.open(file_list).to_a

      @available_dbs = Hash.new()

      files.each do |file|
	next unless file.chomp!
	next unless file.end_with?(".tar.gz")
	full_name = file.split[-1]
	db_name = full_name.split('.')[0]
	(@available_dbs[db_name] ||= []) << full_name
      end

      return @available_dbs.keys.join("\n")
    end

    def download(db_list)
      list()

      dbname_list = []
      md5_list = []
      db_list.each do |db| 
	if not @available_dbs.has_key?(db)
	  $stderr.puts "#{db} is not exists"
	  next
	end

	@available_dbs[db].each do |dbname|
	  md5_list << dbname + '.md5'
	end
      end

      # Download md5 files
      `lftp #{@ftp_address} -e 'cd #{@dir}; mget #{md5_list.join(" ")}; exit'`

      # md5 cache
      md5_cache_dir = 'md5_old'
      if not File.exists?(md5_cache_dir)
	FileUtils.mkdir(md5_cache_dir)
      end

      # Check if these files are really need to update
      md5_list.each do |md5_file|
	md5_old = File.join(md5_cache_dir, md5_file)
	if File.exists?(md5_old)
	  if File.read(md5_old).chomp! == File.read(md5_file).chomp!
	    next
	  end
	end

	dbname_list << md5_file[0...-4]
      end

      # Download files
      if dbname_list.size > 0
	`lftp #{@ftp_address} -e 'cd #{@dir}; pget -n 10 #{dbname_list.join(" ")}; exit'`
	$stdout.puts "Downloading #{dbname_list.join(' ')}"
      else
	$stdout.puts "Your databases are already updated!"
      end

      # Cache md5 files
      FileUtils.mv(Dir.glob('*.md5'), md5_cache_dir, :force => true, :verbose => true)
    end
  end

  class Ncbi
    include DbProcess

    def initialize
      ftp = "ftp.ncbi.nlm.nih.gov"
      blast_db_dir = "blast/db"
      set_up(ftp, blast_db_dir)
    end
  end
end
