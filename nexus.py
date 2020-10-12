import flask
import json
from flask import request
import sys


stream = list()
max_bytes = 256 * 1024 * 1024  # TODO implement max memory size
max_stream_size = 100  # TODO parameterize both of these


app = flask.Flask('nexus')


@app.route('/', methods=['POST'])
def add_msg():
    payload = request.json
    stream.append(payload)
    print('SOURCE:', request.remote_addr, 'META:', payload['meta'], 'SIZE:', sys.getsizeof(stream), 'COUNT:', len(stream))
    if (len(stream) > max_stream_size)
        del stream[0]  # prevent stream from getting too big
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@app.route('/<count>', methods=['GET'])    
def fetch_msg(count):
    result = stream[-count:]
    print('DESTINATION:', request.remote_addr, 'COUNT:', count)
    return flask.Response(json.dumps(result), mimetype='application/json')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)  # TODO parameterize this