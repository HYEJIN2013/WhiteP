
    ## This creates the database instance
    connection = Fog::Rackspace::Databases.new({
      :rackspace_username   => RACKSPACE_USERNAME,
      :rackspace_api_key    => RACKSPACE_API_KEY
    })
    
    database_instance = connection.instances.create({
     :name => database_server.name, 
     :flavor_id => 2, 
     :volume_size => 1 
    })

    # I want to wait here until the server is built. 

    database_server.instance_id = database_instance.id
    database_server.hostname = database_instance.hostname
    database_server.save
