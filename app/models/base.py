from sqlalchemy.ext.declarative import declarative_base
from app.config.db import get_engine
from random import randint 

Base = declarative_base()
