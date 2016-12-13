#!/usr/bin/env ruby

require 'terminal-notifier'

case ARGV.first
when "mongo"
  title = "MongoDB"
  running = `launchctl list | grep mongodb`
  if running == ""
    system('launchctl load -w ~/Library/LaunchAgents/homebrew.mxcl.mongodb.plist') ? message = "#{title} has been started." : message = "An error has occured."
  else
    system('launchctl unload -w ~/Library/LaunchAgents/homebrew.mxcl.mongodb.plist') ? message = "#{title} has been stopped." : message = "An error has occured."
  end
when "mysql"
  title = "MySQL"
  running = `launchctl list | grep mysql`
  if running == ""
    system('launchctl load -w ~/Library/LaunchAgents/homebrew.mxcl.mysql.plist') ? message = "#{title} has been started." : message = "An error has occured."
  else
    system('launchctl unload -w ~/Library/LaunchAgents/homebrew.mxcl.mysql.plist') ? message = "#{title} has been stopped." : message = "An error has occured."
  end
when "redis"
  title = "Redis"
  running = `launchctl list | grep redis`
  if running == ""
    system('launchctl load -w ~/Library/LaunchAgents/homebrew.mxcl.redis.plist') ? message = "#{title} has been started." : message = "An error has occured."
  else
    system('launchctl unload -w ~/Library/LaunchAgents/homebrew.mxcl.redis.plist') ? message = "#{title} has been stopped." : message = "An error has occured."
  end
when "postgre"
  title = "PostgreSQL"
  running = `launchctl list | grep postgresql`
  if running == ""
    system('launchctl load -w ~/Library/LaunchAgents/homebrew.mxcl.postgresql.plist') ? message = "#{title} has been started." : message = "An error has occured."
  else
    system('launchctl unload -w ~/Library/LaunchAgents/homebrew.mxcl.postgresql.plist') ? message = "#{title} has been stopped." : message = "An error has occured."
  end 
else
  title = "Error"
  message = "Unknown database" 
end

TerminalNotifier.notify(message, :title => title)
