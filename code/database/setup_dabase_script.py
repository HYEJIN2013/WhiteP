engine = create_engine('sqlite:///', echo = True)

def setUpDatabase():
  global data #This is global since it is referenced in the tear down method as well.
  dbfixture = SQLAlchemyFixture(
    engine = engine,
    env = {
      'WarehouseFixture' : Warehouse,
      'SectionFixture' : Section
    }
  )
  data = dbfixture.data(WarehouseFixture, SectionFixture)
  data.setup()
