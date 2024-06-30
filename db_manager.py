from models import Window, Session, Base, BaseModel
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from abc import ABC


class DB:
    engine = create_engine('sqlite:///database.db')
    _session = sessionmaker(bind=engine)()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DB, cls).__new__(cls)
        return cls.instance

    @property
    def session(self):
        if not self.tables_exists():
            self.create_tables()
        return self._session

    def tables_exists(self):
        _inspect = inspect(self.engine)
        return _inspect.has_table(Window.__tablename__) and _inspect.has_table(Session.__tablename__)

    def create_tables(self):
        Base.metadata.create_all(self.engine)


class DBManager(ABC):
    _type: BaseModel = None
    _db = DB()

    def __init__(self):
        self._session = self._db.session

    @property
    def session(self):
        return self._session

    def get_all(self):
        return self.session.query(self._type).all()

    def get_by_id(self, entity_id):
        return self.session.query(self._type).filter(self._type.id == entity_id).first()

    def add(self, entity):
        self.session.add(entity)
        self.session.commit()


class WindowDBManager(DBManager):
    _type = Window

    def get_by_fullname(self, fullname):
        return self.session.query(self._type).filter(self._type.fullname == fullname).first()


class SessionDBManager(DBManager):
    _type = Session
