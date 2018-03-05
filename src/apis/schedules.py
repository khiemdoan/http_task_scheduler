from flask import Blueprint
from flask import request
from .response import success, fail
from processors import ScheduleManager


service = Blueprint('schedules', __name__, url_prefix='/schedules')


@service.route('', methods=['GET'])
def get_all():
    manager = ScheduleManager()
    schedules = manager.list()
    schedules = [s.serialize() for s in schedules]
    return success(schedules=schedules)


@service.route('', methods=['POST'])
def add():
    request_info = request.get_json()

    name = request_info.get('name')
    time = request_info.get('time')
    method = request_info.get('method')
    uri = request_info.get('uri')
    parameters = request_info.get('parameters')
    comment = request_info.get('comment')

    manager = ScheduleManager()
    try:
        schedule, errors = manager.add(name, time, method, uri, parameters, comment)
        return success(schedule=schedule.serialize())
    except Exception as ex:
        return fail(schedule=None, errors=ex.args)


@service.route('/<int:schedule_id>')
def get(schedule_id):
    manager = ScheduleManager()
    schedule = manager.get(schedule_id)
    return success(schedule=schedule)


@service.route('/<int:schedule_id>', methods=['DELETE'])
def delete(schedule_id):
    manager = ScheduleManager()
    result = manager.delete(schedule_id)
    if result:
        return success()
    return fail()


@service.route('/<int:schedule_id>', methods=['PUT'])
def update(schedule_id):
    request_info = request.get_json()

    name = request_info.get('name')
    time = request_info.get('time')
    method = request_info.get('method')
    uri = request_info.get('uri')
    parameters = request_info.get('parameters')
    comment = request_info.get('comment')

    manager = ScheduleManager()
    schedule = manager.update(schedule_id, name, time, method, uri, parameters, comment)

    return success(schedule=schedule)
