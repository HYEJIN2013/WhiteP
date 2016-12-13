 ## This creates the database and user
    connection = Fog::Rackspace::Databases.new({
      :rackspace_username   => RACKSPACE_USERNAME,
      :rackspace_api_key    => RACKSPACE_API_KEY
    })
    
    domain_database = connection.database.create({
      :instance_id => domain.database_server.instance_id,
      :name => domain.username
    })
    
    database_user = connection.user.create({
      :instance_id => domain.database_server.instance_id,
      :name => domain.db_username,
      :password => domain.db_password
    })
