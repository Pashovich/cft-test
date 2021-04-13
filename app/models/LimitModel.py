from sqlalchemy import Column, DateTime, String, Integer, func
from .base import Base, randint, get_engine


def random_integer():
    min_ = 100
    max_ = 1000000000
    rand = randint(min_, max_)

    from sqlalchemy.orm import sessionmaker
    db_session_maker = sessionmaker(bind=get_engine())
    db_session = db_session_maker()
    print('here')
    while db_session.query(Limits).filter(Limits.client_id == rand).limit(1).first() is not None:
        print('asdadasdasdasdasd')
        rand = randint(min_, max_)

    return rand


class Limits(Base):
    __tablename__ = 'limits'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, unique=False, default = random_integer)
    country = Column(String)
    cur = Column(String)
    limit = Column(Integer)



    def __repr__(self):
        return f'{self.id}, \
            {self.client_id}, \
            {self.country},\
            {self.cur}, \
            {self.limit}'

    def get_json(self):
        return {
            "client_id": self.client_id,
            "country": self.country,
            "cur": self.cur,
            "limit": self.limit
        }

    def update(self,**kwargs):
        for key, value in kwargs.items():
            setattr(self,key, value)




    