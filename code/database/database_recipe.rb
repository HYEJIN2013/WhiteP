include_recipe "database"

# define database server connection info
connection_info = {
  :host => "localhost",
  :username => 'root',
  :password => node['mysql']['server_root_password']
}

# create database
database 'test3' do
  connection connection_info
  provider "Chef::Provider::Database::#{node[:provider]}"
  action :create
end
