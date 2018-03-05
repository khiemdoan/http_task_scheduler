from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import BaseModel


Session = sessionmaker()


class Connector:

    def __init__(self):
        engine = create_engine('sqlite:///database.db')
        BaseModel.metadata.bind = engine
        BaseModel.metadata.create_all(engine)
        Session.configure(bind=engine)
        self._session = Session()
