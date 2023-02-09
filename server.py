import argparse
import logging
from flask import Flask, render_template, request
from flask_cors import CORS

from utils import set_logging_level
from json_filter_bot import JsonFilterBot


bot = JsonFilterBot()

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/json_filter', methods=['POST'])
def json_filter():
    logging.debug('***************** /json_filter **********************')
    logging.debug(f'request.data:\n{request.data}')
    data = request.get_json()
    logging.debug(f'data json loaded:\n{data}')

    if 'nl_query' not in data:
        raise ValueError('missing nl_query aparam')
    nl_query = data['nl_query']
    space_functions = data.get('space_functions')
    response = build_json_filter(nl_query, space_functions=space_functions)
    logging.debug('*****************************************************')
    return response


def build_json_filter(nl_query, space_functions=None):
    response = bot(nl_query, space_functions=space_functions)
    return response


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--log_level', type=str, default='info', help="Must be in ('info', 'error', 'debug')")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    log_level = args.log_level
    set_logging_level(log_level=log_level)

    app.run(debug=True, use_reloader=True, host='0.0.0.0', port=5050)
