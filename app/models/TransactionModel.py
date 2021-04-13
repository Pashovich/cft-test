from sqlalchemy import Column, DateTime, String, Integer, func
from .base import Base, randint, get_engine
import time

def random_integer(self):
    min_ = 100
    max_ = 1000000000
    rand = randint(min_, max_)

    from sqlalchemy.orm import sessionmaker
    db_session_maker = sessionmaker(bind=get_engine())
    db_session = db_session_maker()
    while db_session.query(Transactions).filter(Transactions.client_id == rand).one() is not None:
        rand = randint(min_, max_)

    return rand

class Transactions(Base):

    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, unique=False,  default = random_integer)
    country = Column(String)
    cur = Column(String)
    amount = Column(Integer)
    date = Column(DateTime(timezone=True), default=func.now())

    def update(self,**kwargs):
        for key, value in kwargs.items():
            setattr(self,key, value)

    def get_json(self):
        return {
            "client_id": self.client_id,
            "country": self.country,
            "cur": self.cur,
            "amount": self.amount,
            "date": int(time.mktime(self.date.timetuple()))
        }

    def __repr__(self):
        return f'{self.id},\
            {self.client_id},\
            {self.cur},\
            {self.country},\
            {self.amount},\
            {self.date}'


