#!/usr/bin/python3
"""
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.base_model import Base

if getenv('HBNB_TYPE_STORAGE') == 'db':
    from models.place import place_amenity

classes = [User, State, City, Place, Amenity, Review]


class DBStorage:
    """
    Creates a database storage engine
    """
    __engine = None
    __session = None

    def __init__(self):
        """Instantiates the engine"""
        HBNB_MYSQL_USER = getenv("HBNB_MYSQL_USER")
        HBNB_MYSQL_PWD = getenv("HBNB_MYSQL_PWD")
        HBNB_MYSQL_HOST = getenv("HBNB_MYSQL_HOST")
        HBNB_MYSQL_DB = getenv("HBNB_MYSQL_DB")
        HBNB_ENV = getenv("HBNB_ENV")
        self.__engine = create_engine(f"""
                                      mysql+mysqldb://{HBNB_MYSQL_USER}:
                                      {HBNB_MYSQL_PWD}@{HBNB_MYSQL_HOST}/
                                      {HBNBN_MYSQL_DB}""", pool_pre_ping=True)
        if HBNB_ENV == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on current db session all objects depending on class name"""
        dct = {}
        if cls is None:
            for c in classes:
                objs = self.__session.query(c).all()
                for obj in objs:
                    key = obj.__class__.name + '.' + obj.id
                    dct[key] = obj

        else:
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = obj.__class__.name + '.' + obj.id
                dct[key] = obj

        return (dct)

    def new(self, obj):
        """Add object to current db session"""
        if obj is not None:
            try:
                self.__session.add(obj)
                self.__session.flush()
                self.__session.refresh(obj)
            except Exception as e:
                self.__session.rollback()
                raise e

    def save(self):
        """Commit all changes of current db session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from current db session obj if not None"""
        if obj is not None:
            self.__session.query(type(obj)).
            filter(type(obj).id == obj.id).delete()

    def reload(self):
        """Reloads the db"""
        Base.metadata.create_all(self.__engine)
        create_session = sessionmaker(bind=self.__engine,
                                      expire_on_commit=False)
        self.__session = scoped_session(create_session)()

    def close(self):
        """Close current session"""
        self.__session.close()