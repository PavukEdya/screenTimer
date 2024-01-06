from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, Time
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


class Window(BaseModel):
    __tablename__ = 'window'

    name = Column(String)
    fullname = Column(String)


class Session(BaseModel):
    __tablename__ = 'session'

    window_id = ForeignKey('window.id')
    time = Column(Time)

    window = relationship('Window',back_populates='sessions')
