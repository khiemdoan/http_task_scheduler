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

    if request_info is None:
        return fail(schedule=None, errors=['You need pass more parameters.'])

    name = request_info.get('name')
    time = request_info.get('time')
    method = request_info.get('method')
    uri = request_info.get('uri')
    parameters = request_info.get('parameters')
    comment = request_info.get('comment')

    manager = ScheduleManager()
    try:
        schedule = manager.add(name, time, method, uri, parameters, comment)
        return success(schedule=schedule.serialize())
    except ValueError as ex:
        return fail(schedule=None, errors=ex.args)


@service.route('/<int:schedule_id>')
def get(schedule_id):
    manager = ScheduleManager()
    schedule = manager.get(schedule_id)
    return success(schedule=schedule.serialize())


@service.route('/name/<string:schedule_name>')
def get_by_name(schedule_name):
    schedules = ScheduleManager().get_by_name(schedule_name)
    schedules = [s.serialize() for s in schedules]
    return success(schedules=schedules)


@service.route('/<int:schedule_id>', methods=['DELETE'])
def delete(schedule_id):
    manager = ScheduleManager()
    result = manager.delete(schedule_id)
    if result:
        return success()
    return fail()


@service.route('/name/<string:schedule_name>', methods=['DELETE'])
def delete_by_name(schedule_name):
    result = ScheduleManager().delete_by_name(schedule_name)
    return success() if result else fail()


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

    return success(schedule=schedule.serialize())


@service.route('/name/<string:schedule_name>', methods=['PUT'])
def update_by_name(schedule_name):
    request_info = request.get_json()

    name = request_info.get('name')
    time = request_info.get('time')
    method = request_info.get('method')
    uri = request_info.get('uri')
    parameters = request_info.get('parameters')
    comment = request_info.get('comment')

    manager = ScheduleManager()
    schedules = manager.update_by_name(schedule_name, name, time, method, uri, parameters, comment)
    schedules = [s.serialize() for s in schedules]

    return success(schedules=schedules)
