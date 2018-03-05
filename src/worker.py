import os
import argparse
import requests
import json
import logging

from database import Connector as DbConnector


logging_level = logging.NOTSET if __name__ == '__main__' else logging.WARNING
logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging_level,
)


def get_worker_file():
    return __file__


def run_schedule(schedule_id: int):
    if not isinstance(schedule_id, int):
        return

    db = DbConnector()
    schedule = db.get_schedule(schedule_id)
    if schedule is None:
        return

    method = schedule.method
    try:
        parameters = json.loads(schedule.parameters)
        if isinstance(parameters, dict):
            parameters = {str(k): str(v) for k, v in parameters.items()}
        else:
            parameters = None
    except json.JSONDecodeError:
        parameters = None

    if method.upper() == 'GET':
        requests.request(schedule.method, schedule.uri, params=parameters)
    else:
        requests.request(schedule.method, schedule.uri, json=parameters)


if __name__ == '__main__':
    current_dir = os.path.dirname(__file__)
    current_dir = os.path.abspath(current_dir)
    os.chdir(current_dir)

    parser = argparse.ArgumentParser(description='Schedule Worker')
    parser.add_argument("schedule", help="Schedule id", type=int, nargs=1)
    args = parser.parse_args()

    run_schedule(args.schedule[0])
