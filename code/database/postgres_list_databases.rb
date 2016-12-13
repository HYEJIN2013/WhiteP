require "rubygems"
require "active_record"
require 'logger'

ActiveRecord::Base.establish_connection(
                                        :adapter => 'postgresql',
                                        :database => '<db_name>',
                                        :username => '<user>',
                                        :password => '<pass>',
                                        :host => '/var/run/postgresql')

ActiveRecord::Base.logger = Logger.new('logfile.txt')
databases = ActiveRecord::Base.connection.query("select datname from pg_database")
#=> [["template1"], ["template0"], ["postgres"], ["testdb"]]
