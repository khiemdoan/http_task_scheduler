from typing import List
from crontab import CronTab
import json

from database import ScheduleConnector as DbConnector
from database.models import Schedule
from worker import get_worker_file



class ScheduleManager:
    """Job manager"""

    def __init__(self) -> None:
        self._db = DbConnector()

    def list(self) -> List[Schedule]:
        """Get all schedules"""
        return self._db.get_all_schedule()

    def add(self, name: str, time: str, method: str, uri: str,
            parameters: str, comment: str) -> Schedule:
        """Add a schedule"""
        errors = []

        if not isinstance(time, str) or len(time) == 0:
            errors.append('Time must be string and not empty')
        if not isinstance(method, str) or len(time) == 0:
            errors.append('Method must be string and not empty')
        if not isinstance(uri, str) or len(time) == 0:
            errors.append('Uri must be string and not empty')

        if len(errors):
            raise ValueError(errors)

        if not isinstance(name, str):
            name = ''
        try:
            parameters = json.dumps(parameters)
        except TypeError:
            parameters = ''
        if not isinstance(comment, str):
            comment = ''

        schedule = self._db.add_schedule(name, time, method, uri, parameters, comment)
        self._update_cron()
        return schedule

    def get(self, schedule_id: int) -> Schedule:
        return self._db.get_schedule(schedule_id)

    def get_by_name(self, name: str) -> List[Schedule]:
        return self._db.get_schedules_by_name(name)

    def delete(self, schedule_id: int) -> bool:
        """Delete a schedule"""
        result = self._db.delete_schedule(schedule_id)
        self._update_cron()
        return result

    def delete_by_name(self, name) -> bool:
        result = self._db.delete_schedule_by_name(name)
        self._update_cron()
        return result

    def update(self, schedule_id: int,
               name: str, time: str, method: str, uri: str,
               parameters: str, comment: str) -> Schedule:
        schedule = self._db.get_schedule(schedule_id)
        if isinstance(name, str) and len(name):
            schedule.name = name
        if isinstance(time, str) and len(time):
            schedule.time = time
        if isinstance(method, str) and len(method):
            schedule.method = method
        if isinstance(uri, str) and len(uri):
            schedule.uri = uri
        if isinstance(parameters, str) and len(parameters):
            schedule.parameters = parameters
        if isinstance(comment, str) and len(comment):
            schedule.comment = comment
        self._db.update_schedule()
        self._update_cron()
        return schedule

    def update_by_name(self, schedule_name: str,
                       name: str, time: str, method: str, uri: str,
                       parameters: str, comment: str) -> List[Schedule]:
        schedules = self._db.get_schedules_by_name(schedule_name)
        for schedule in schedules:
            if isinstance(name, str) and len(name):
                schedule.name = name
            if isinstance(time, str) and len(time):
                schedule.time = time
            if isinstance(method, str) and len(method):
                schedule.method = method
            if isinstance(uri, str) and len(uri):
                schedule.uri = uri
            if isinstance(parameters, str) and len(parameters):
                schedule.parameters = parameters
            if isinstance(comment, str) and len(comment):
                schedule.comment = comment
        self._db.update_schedule()
        self._update_cron()
        return schedules

    def _update_cron(self) -> None:
        """Update crontab follow database"""
        cron = CronTab(user=True)
        cron.remove_all()

        worker = get_worker_file()

        schedules = self.list()
        for schedule in schedules:
            command = 'python3 {} {}'.format(worker, schedule.id)
            job = cron.new(command=command, comment=schedule.name)
            job.setall(schedule.time)
            job.enable(schedule.enable)
            cron.write()
