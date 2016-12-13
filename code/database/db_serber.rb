include_recipe "mysql::ruby"
include_recipe "mysql::server"

#---------------------------------------------------------------------
# Enable mysql service
#---------------------------------------------------------------------

service "mysql" do
  action :enable
end

#---------------------------------------------------------------------
# Setup db
#---------------------------------------------------------------------

mysql_connection_info = {
  :host => "localhost",   
  :username => 'root', 
  :password => node[:mysql][:server_root_password]
}

db_config = node[:databases][:test]

mysql_database db_config[:database] do
  connection mysql_connection_info
  action :create
end

#---------------------------------------------------------------------
# Create db user
#---------------------------------------------------------------------

mysql_database_user db_config[:username] do
  database_name db_config[:database]
  connection mysql_connection_info
  password db_config[:password]  
  host '%'   
  action :grant
end
