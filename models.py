from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, DateTime, CheckConstraint
from sqlalchemy.orm import relationship, DeclarativeBase, declarative_base
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


class Window(BaseModel):
    __tablename__ = 'window'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    fullname = Column(String, nullable=False)

    sessions = relationship('Session', back_populates='window')


class Session(BaseModel):
    __tablename__ = 'session'

    id = Column(Integer, primary_key=True)
    window_id = Column(Integer, ForeignKey('window.id', ondelete='CASCADE'), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    window = relationship('Window', back_populates='sessions')

    __table_args__ = (
        CheckConstraint('start_time < end_time', name='start_end_check'),
    )
