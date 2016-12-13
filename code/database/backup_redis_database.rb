#! /usr/bin/env ruby
#
# -*- mode: ruby -*-
# Backup Redis database
#
# This should be placed in the crontab, as in the following example
# (hourly backups)
#
#    0 * * * * /path/to/backup
#

require "redis"
require "fileutils"
require "s4"

ROOT = File.expand_path("../..", __FILE__)

def root file
  File.join(ROOT, file)
end

s3file = File.join ROOT, '.s3'
abort "Add S3 URL to #{s3file}" unless File.exists?(s3file)

def redis
  @redis ||= Redis.new url: ENV["REDIS_URL"]
end

def not_happening action, delay=0.2
  while redis.info[action] == "1"
    sleep delay
  end
end

# Make sure it's not rewriting AOF already
not_happening "bgwriteaof_in_progress"

# Make sure it's not in BGSAVE mode
not_happening "bgsave_in_progress"

# Background save
redis.bgsave

# Wait
not_happening "bgsave_in_progress", 1

# Create backup file
timestamp   = Time.now.strftime "%Y%m%d%H%M%S"
source      = root("db/dump.rdb")
destination = root("tmp/#{timestamp}.dump.rdb")

FileUtils.cp source, destination

puts "Redis backup saved to #{destination}"

# Upload latest backup to S3
bucket        = S4.connect url: open(s3file).read
s3destination = "#{ENV["BUCKET"]}/#{timestamp}.dump.rdb"
bucket.upload destination, s3destination

puts "Redis backup uploaded to #{s3destination}"

# Delete local backup
FileUtils.rm destination
