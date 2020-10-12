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
            print('PROCESS bytes:', size_bytes, 'STREAM count:', len(stream), 'PID:', os.getpid())  # debug output
            return
    

@app.route('/', methods=['POST'])
def add_msg():
    payload = request.json
    stream.append(payload)
    print('RECEIVED from:', request.remote_addr, 'META:', payload['meta'])
    trim_stream()  # prevent unlimited growth of stream of consciousness
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@app.route('/fetch', methods=['GET'])    
def fetch_msg():
    result = stream
    # filter based on type
    if 'type' in request.args:
        result = [i for i in result if request.args['type'] in i['meta']['type']]    
    # filter based on max results
    if 'maxresults' in request.args:
        result = result[-int(request.args['maxresults']):]
    else:
        result = result[-5:]  # return only last 5 by default
    print('FETCH from:', request.remote_addr, 'QUERY:', request.query_string.decode(), 'COUNT:', len(result))
    return flask.Response(json.dumps(result), mimetype='application/json')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)  # TODO parameterize this