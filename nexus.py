from time import time
from uuid import uuid4
import flask
import json
from flask import request
import os
import psutil
import logging

stream = list()  # stream of consciousness
#max_bytes = 2 * 1024 * 1024 * 1024  # 2GB
max_bytes = 100 * 1024 * 1024 # 100MB


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
            #print('PROCESS bytes:', size_bytes, 'STREAM count:', len(stream), 'PID:', os.getpid())  # debug output
            return
    

@app.route('/', methods=['POST', 'GET'])
def api():
    try:
        if request.method == 'POST':
            payload = request.json
            # required: message (msg), key, service id (sid)
            new = dict()
            new['msg'] = payload['msg']
            new['key'] = payload['key']
            new['sid'] = payload['sid']
            new['mid'] = str(uuid4())  # add message ID
            new['time'] = time()  # add timestamp
            # TODO - add detection for misbehaving services
            stream.append(payload)
            trim_stream()  # prevent unlimited growth of stream of consciousness
            print('POST:', payload['msg'][0:40])
            return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
        elif request.method == 'GET':
            result = stream
            # filter stream
            if 'keyword' in request.args:
                result = [i for i in result if request.args['keyword'] in str(i)]
            if 'start' in request.args:
                result = [i for i in result if i['time'] >= float(request.args['start'])]
            if 'end' in request.args:
                result = [i for i in result if i['time'] <= float(request.args['end'])]
            print('GET:', request.query_string.decode(), '\tCOUNT:', len(result))
            return flask.Response(json.dumps(result), mimetype='application/json')
        elif request.method == 'DELETE':
            # TODO add delete functionality, pruning the stream is necessary for speed and hygiene
            print('DELETE:', str(request))
            return json.dumps({'success':False}), 404, {'ContentType':'application/json'} 
    except Exception as oops:
        print(oops)
        return json.dumps({'success':False}), 500, {'ContentType':'application/json'} 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)