import flask
import json
from flask import request
import os
import logging
import numpy as np
from uuid import uuid4
from time import time


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app = flask.Flask('nexus')


def load_data():
    files = os.listdir('logs/')
    result = list()
    for file in files:
        with open('logs/%s' % file, 'r', encoding='utf-8') as infile:
            result.append(json.load(infile))
    return result
    

def save_log(payload):
    filename = payload['uuid'] + '.json'
    with open('logs/%s' % filename, 'w', encoding='utf-8') as outfile:
        #json.dump(payload, outfile, indent=1, ensure_ascii=False, sort_keys=True)
        json.dump(payload, outfile, ensure_ascii=False, sort_keys=True)


@app.route('/add', methods=['POST'])  # register new message
def add():  # REQUIRED: content, vector, microservice?
    try:
        payload = request.json
        payload['time'] = time()
        payload['uuid'] = str(uuid4())
        # TODO - handle vector here? 
        # TODO - microservice?
        # TODO - validate message payload
        save_log(payload)
        print(payload)
        return 'successfully added record', 200, {'ContentType':'application/json'}
    except Exception as oops:
        print(oops)
        return str(oops), 500, {'ContentType':'application/json'}


@app.route('/search', methods=['POST'])  # return n number of top semantic matches
def search():  # REQUIRED: vector, count
    try:
        results = list()
        payload = request.json
        count = payload['count']
        vector = payload['vector']
        data = load_data()
        for i in data:
            try:
                score = np.dot(i['vector'], vector)
                info = i
                info['score'] = score
                results.append(info)
            except Exception as oops:
                print(oops)
                continue
        ordered = sorted(results, key=lambda d: d['score'], reverse=True)
        try:  # just hack off the ordered list
            ordered = ordered[0:count]
            return json.dumps(ordered), 200, {'ContentType':'application/json'}
        except:  # if it barfs, send back the whole list because it's too short
            return json.dumps(ordered), 200, {'ContentType':'application/json'}
    except Exception as oops:
        print(oops)
        return str(oops), 500, {'ContentType':'application/json'}


@app.route('/match', methods=['POST'])  # retrieve all messages that have a matching field/value pair
def match():  # REQUIRED: field, value
    try:
        results = list()
        payload = request.json
        data = load_data()
        field = payload['field']  # which field to search each record for
        value = payload['value']  # value of field to match
        results = [i for i in data if i[field] == value]
        ordered = sorted(results, key=lambda d: d[sortby], reverse=reverse)
        try:
            ordered = ordered[0:count]
            return json.dumps(ordered), 200, {'ContentType':'application/json'}
        except:
            return json.dumps(ordered), 200, {'ContentType':'application/json'}
    except Exception as oops:
        print(oops)
        return str(oops), 500, {'ContentType':'application/json'}


@app.route('/bound', methods=['POST'])  # retrieve all messages between two timestamps
def bound():  # REQUIRED: upper_bound, lower_bound
    try:
        results = list()
        payload = request.json
        data = load_data()
        lower_bound = payload['lower_bound']
        upper_bound = payload['upper_bound']
        for i in data:
            try:
                if i['time'] >= lower_bound and i['time'] <= upper_bound:
                    results.append(i)
            except:
                continue
        return json.dumps(results), 200, {'ContentType':'application/json'}
    except Exception as oops:
        print(oops)
        return str(oops), 500, {'ContentType':'application/json'}


@app.route('/recent', methods=['POST'])
def recent():
    try:
        payload = request.json
        seconds = payload['seconds']
        min_age = time() - seconds
        data = load_data()
        results = [i for i in data if i['time'] >= min_age]
        return json.dumps(results), 200, {'ContentType':'application/json'}
    except Exception as oops:
        print(oops)
        return str(oops), 500, {'ContentType':'application/json'}
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)