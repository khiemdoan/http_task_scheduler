from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import BaseModel
from .models import Schedule


Session = sessionmaker()


class Connector:

    def __init__(self):
        engine = create_engine('sqlite:///database.db')
        BaseModel.metadata.bind = engine
        BaseModel.metadata.create_all(engine)
        Session.configure(bind=engine)
        self._session = Session()

    def add_schedule(self, name: str, time: str, method: str,
                     uri: str, parameters: str, comment: str) -> Schedule:
        schedule = Schedule(
            name=name,
            time=time,
            method=method,
            uri=uri,
            parameters=parameters,
            comment=comment,
        )
        self._session.add(schedule)
        self._session.commit()
        return schedule

    def get_all_schedule(self) -> List[Schedule]:
        return self._session.query(Schedule).all()

    def get_schedule(self, schedule_id: int) -> Schedule:
        return self._session.query(Schedule).get(schedule_id)

    def delete_schedule(self, schedule_id) -> bool:
        schedule = self.get_schedule(schedule_id)
        if isinstance(schedule, Schedule):
            self._session.delete(schedule)
            self._session.commit()
            return True
        return False

    def update_schedule(self):
        self._session.commit()
