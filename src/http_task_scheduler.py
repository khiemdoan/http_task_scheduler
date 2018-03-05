import os
import logging

from flask import Flask
from apis import schedule_service


logging_level = logging.NOTSET if __name__ == '__main__' else logging.WARNING
logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging_level,
)

current_dir = os.path.dirname(__file__)
current_dir = os.path.abspath(current_dir)
os.chdir(current_dir)


app = Flask(__name__)
app.register_blueprint(schedule_service)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000, debug=True)
