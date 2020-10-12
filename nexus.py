import flask
import json
from flask import request
import os
import psutil
import logging

stream = list()  # stream of consciousness
max_bytes = 2 * 1024 * 1024 * 1024  # TODO parameterize this
#max_bytes = 100000000  # debug size


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app = flask.Flask('nexus')


def trim_stream():
    process = psutil.Process(os.getpid())
    while True:
        size_bytes = process.memory_info().rss
        if size_bytes > max_bytes:
            del stream[0]
        else:
            print('process bytes:', size_bytes, 'stream count:', len(stream), 'pid:', os.getpid())  # debug output
            return
    

@app.route('/', methods=['POST'])
def add_msg():
    payload = request.json
    stream.append(payload)
    print('message received from:', request.remote_addr, 'META:', payload['meta'])
    trim_stream()  # prevent unlimited growth of stream of consciousness
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@app.route('/fetch', methods=['GET'])    
def fetch_msg():
    result = stream
    # filter based on query
    if 'type' in request.args:
        result = [i for i in result if request.args['type'] in i['meta']['type']]    
    if 'maxresults' in request.args:
        result = result[-int(request.args['maxresults']):]
    else:
        result = result[-5:]  # return only last 5 by default
    print('fetch from:', request.remote_addr, 'query:', request.query_string.decode(), 'count:', len(result))
    return flask.Response(json.dumps(result), mimetype='application/json')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)  # TODO parameterize this