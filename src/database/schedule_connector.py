from typing import List
from .connector import Connector
from .models.schedule import Schedule


class ScheduleConnector(Connector):

    def __init__(self):
        super().__init__()

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

    def get_schedules_by_name(self, name: str) -> List[Schedule]:
        return self._session.query(Schedule).filter_by(name=name).all()

    def delete_schedule(self, schedule_id) -> bool:
        schedule = self.get_schedule(schedule_id)
        if isinstance(schedule, Schedule):
            self._session.delete(schedule)
            self._session.commit()
            return True
        return False

    def update_schedule(self):
        self._session.commit()

