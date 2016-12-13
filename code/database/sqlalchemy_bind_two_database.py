from sqlalchemy import (String,
                        Integer,
                        engine_from_config,
                        Column)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base_1 = declarative_base()

Base_2 = declarative_base()


class City(Base_1):
    __tablename__ = 'citys'
    id = Column(Integer, primary_key=True)
    level = Column(Integer, nullable=False)
    name = Column(String, nullable=False)


class NewCity(Base_2):
    __tablename__ = 'new_citys'
    id = Column(Integer, primary_key=True)
    level = Column(Integer, nullable=False)
    name = Column(String, nullable=False)


config_1 = {
    "sqlalchemy.url": "postgresql:///t1",
    "sqlalchemy.echo": False,
}
config_2 = {
    "sqlalchemy.url": "postgresql:///t2",
    "sqlalchemy.echo": False,
}
engine_1 = engine_from_config(config_1)
engine_2 = engine_from_config(config_2)
Base_2.metadata.drop_all(bind=engine_2)
Base_1.metadata.drop_all(bind=engine_1)
Base_1.metadata.create_all(bind=engine_1)
Base_2.metadata.create_all(engine_2)
Session = sessionmaker(twophase=True)
Session.configure(binds={City: engine_1, NewCity: engine_2})
session = Session()
city = City(id=1, level=1, name="xxx")
new_city = NewCity(id=1, level=2, name="yyyy")
try:
    session.add(city)
    session.add(new_city)
    session.commit()
except Exception as e:
    session.rollback()
try:
    city = City(id=1, level=1, name="xxx")
    new_city = NewCity(id=2, level=2, name="yyyyy")

    session.add(new_city)
    session.add(city)
    session.commit()
except Exception as e:
    print(e)
