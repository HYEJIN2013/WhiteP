class MySQL(object):
  __Instance = None

  # Initializer.
  def __init__(self):
    if self.__class__.__Instance:
      return
    else:
      self.__class__.__Instance = self
    self.Conf = DBConf()['MySQL']
    self.Engine = create_engine(
      'mysql+mysqldb://'+self.Conf['User']+':'+self.Conf['Password']+'@'+self.Conf['Host']+':'+str(self.Conf['Port'])+'/'+self.Conf['Database']+'?charset=utf8&use_unicode=0',
      pool_size=10,
      pool_recycle=3600,
      max_overflow=0,
      echo=False
    ).connect()
    self.Engine.execution_options(autocommit=False)

  def __new__(self):
    if self.__Instance:
      return self.__Instance
    else:
      return object.__new__(self)
