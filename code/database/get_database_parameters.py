def get_database_parameters(db_name):
  """ given a database name (db_name), returns a dict with
      host, database, username, password """
  keys = ['hostname', 'database', 'username', 'password']
  values = [dbconfig.get(db_name, x) for x in keys]
  db_params = dict(zip(keys, values))
  return db_params
