current_db = Rails.configuration
  .database_configuration[Rails.env]['database']

sql = ActiveRecord::Base.connection()

all_tables = sql.execute "select TABLE_SCHEMA, TABLE_NAME 
  from information_schema.TABLES 
  where TABLE_SCHEMA = '#{current_db}' 
  and TABLE_NAME <> 'schema_migrations';"

all_tables.each { |schema, table| 
  sql.execute "truncate table #{schema}.#{table}" 
}
