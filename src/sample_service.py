from flask import Flask
from flask import jsonify
from flask import request
from datetime import datetime


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    now = datetime.now()
    args = request.args.to_dict()
    data = request.get_json()

    response = {
        'status': 'success',
        'args': args,
        'data': data,
        'time': now,
    }

    print(response)
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6001, debug=True)
