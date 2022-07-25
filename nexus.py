import flask
import json
from flask import request
import os
import logging
import numpy as np
import pickle


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app = flask.Flask('nexus')


def save(data, filepath='nexus.pickle'):
    with open(filepath, 'wb') as outfile:
        pickle.dump(data, outfile)


def load(filepath='nexus.pickle'):
    with open(filepath, 'wb') as infile:
        data = pickle.load(infile)
    return data


@app.route('/add', methods=['POST'])
def add():  # REQUIRED: time, vector
    global data
    try:
        payload = request.json
        info = payload
        info['time'] = float(payload['time'])
        info['vector'] = np.fromstring(payload['vector'])
        data.append(info)
        save(data)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    except Exception as oops:
        print(oops)
        return json.dumps({'success':False, 'error': oops}), 500, {'ContentType':'application/json'}


@app.route('/search', methods=['POST'])
def search():  # REQUIRED: vector, field, count
    global data
    try:
        results = list()
        payload = request.json
        vector = np.fromstring(payload['vector'])
        field = payload['field']
        count = int(payload['count'])
        for i in data:
            try:
                score = np.dot(i[field], vector)
            except Exception as oops:
                #print(oops)
                continue
            info = i
            info['score'] = score
            results.append(info)
        ordered = sorted(results, key=lambda d: d['score'], reverse=True)
        try:
            ordered = ordered[0:count]
            return ordered, 200, {'ContentType':'application/json'}
        except:
            return ordered, 200, {'ContentType':'application/json'}
    except Exception as oops:
        print(oops)
        return json.dumps({'success':False, 'error': oops}), 500, {'ContentType':'application/json'}


@app.route('/bound', methods=['POST'])
def bound():
    global data
    try:
        results = list()
        payload = request.json
        field = payload['field']
        lower_bound = payload['lower_bound']
        upper_bound = payload['upper_bound']
        for i in self.data:
            try:
                if i[field] >= lower_bound and i[field] <= upper_bound:
                    results.append(i)
            except:
                continue
        return results, 200, {'ContentType':'application/json'}
    except Exception as oops:
        print(oops)
        return json.dumps({'success':False, 'error': oops}), 500, {'ContentType':'application/json'}


if __name__ == '__main__':
    try:
        data = load()
    except:
        data = list()
    app.run(host='0.0.0.0', port=8888)