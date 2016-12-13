require 'activerecord-sqlserver-adapter'

ActiveRecord::Base.establish_connection(
  :adapter => 'sqlserver',
  :mode => 'ODBC',
  :host => '<server>',
  :username => '<user_name>',
  :password => '<pass>'
  :dsn => '<odbc_dsn_name>'
)

databases = ActiveRecord::Base.connection.select_all('select name from sys.databases')
