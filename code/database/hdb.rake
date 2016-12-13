# Tasks for working with your heroku database.
#
# These won't work until you enable the (free) pgbackups addon:
#
# heroku addons:add pgbackups
#
#
# Examples:
#
# Replace development DB with a fresh capture from Heroku
# (removing the oldest one first)
#
# rake hdb:clone # replace development database with a fresh capture of the
#
# choose a different local:
# RAILS_ENV=production rake hdb:clone
#
# choose a different remote:
# HEROKU_APP=the-production-app-name rake hdb:clone

namespace :hdb do
  task(ensure_dropped: 'db:load_config') { drop_database config }

  task(create_one: 'db:load_config') { create_database config }

  desc "capture a backup of the HEROKU_APP database"
  task(:capture) { capture }

  desc "replace the RAILS_ENV database with a fresh capture from HEROKU_APP"
  task clone: [:ensure_dropped, :create_one, :capture] do
    restore
  end

  def capture
    pgbackup 'capture --expire'
  end

  def restore
    print_and_capture %(curl "#{url}" | pg_restore --no-acl --no-owner -U #{username} -d #{database})
  end

  private

  def url
    pgbackup(:url).chomp
  end

  def username
    config['username']
  end

  def database
    config['database']
  end

  def config
    @config ||= ActiveRecord::Base.configurations[environment]
  end

  def environment
    ENV.fetch 'RAILS_ENV', 'development'
  end

  def pgbackup(task=nil)
    sub_command = task ? "pgbackups:#{task}" : 'pgbackups'
    print_and_capture "heroku #{sub_command} --app #{ENV['HEROKU_APP']}"
  end

  def print_and_capture(command)
    puts command
    output = `#{command}`
    exit "non-zero exit status!" if $?.exitstatus != 0
    output
  end
end
