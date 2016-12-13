# Thankfully Rails pprovide a basic interface through ActiveRecord to set up and conenct to multiple databases
# Here is some code for handling two databases (Messages and Users)

#database.yml will hold the info needed to define out databases
db1:
  development:
    adapter: sqlite3
    database: messages_dev
    username: root
db2:
  development:
    adapter: sqlite3
    database: users_dev
    username: root
  
#application.rb will include the following to config our app to load in the db's
db_conf = YAML::load(File.open(File.join(APP_PATH,'config','database.yml')))
DB1 = db_conf["db1"][Rails.env]
DB2 = db_conf["db2"][Rails.env]

# make sure to connect to the right db in each model
#message.rb
class Message < ActiveRecord::Base
  establish_connection DB1
end

#user.rb
class User < ActiveRecord::Base
  establish_connection DB2
end

# for handling migrations it's just a matter of organzing the db/migrate folders
# have migration for messages in a folder called db/migrate/messages for example
namespace :db do
task :migrate do
  Rake::Task["db:migrate_db1"].invoke
end
task :migrate_db1 do
  ActiveRecord::Base.establish_connection DB1
  ActiveRecord::Migrator.migrate("db/migrate/messages/")
end
# the same thing can be done for any number of databases
# testing through RSpec could be sectioned off in a similiar fashion

# the limitations with the above example is that we are not handling the case where we want to access mutiple databases
# at the same time. This can be done with abstract superclass which allows each model to share the conenction pool 
# and transaction blocks:
class SqlBase < ActiveRecord::Base
  establish_connection DB1
  establish_connection DB2
  self.abstract_class = true
end

class User < SqlBase
end

class Message < SqlBase
end

# You have to be careful of how many conenctions you have open so make smart use of
ActiveRecord::Base.clear_all_connections!
