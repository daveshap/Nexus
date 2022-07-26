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


def load(filepath='nexus.pickle'):
    with open(filepath, 'rb') as infile:
        data = pickle.load(infile)
    return data


def jsonify(payload):  # get it ready for output
    if isinstance(payload, dict):
        vector = list(payload['vector'])
        payload['vector'] = vector
        return payload
    elif isinstance(payload, list):
        results = list()
        for i in payload:
            vector = list(i['vector'])
            i['vector'] = vector
            results.append(i)
        return results


def dejsonify(payload):
    vector = payload['vector'].replace('[','').replace(']','')
    payload['vector'] = np.fromstring(vector, dtype=float, sep=',')
    return payload


@app.route('/add', methods=['POST'])
def add():  # REQUIRED: time, vector
    global data
    try:
        payload = request.json
        payload = dejsonify(payload)
        data.append(payload)
        #save(data)
        return 'successfully added record', 200, {'ContentType':'application/json'}
    except Exception as oops:
        print(oops)
        return str(oops), 500, {'ContentType':'application/json'}


@app.route('/search', methods=['POST'])
def search():  # REQUIRED: vector, field, count
    global data
    try:
        results = list()
        payload = request.json
        payload = dejsonify(payload)
        field = payload['field']
        count = payload['count']
        vector = payload['vector']
        for i in data:
            try:
                score = np.dot(i[field], vector)
                info = i
                info['score'] = score
                results.append(info)
            except Exception as oops:
                print(oops)
                continue
        ordered = sorted(results, key=lambda d: d['score'], reverse=True)
        ordered = jsonify(ordered)
        try:
            ordered = ordered[0:count]
            return json.dumps(ordered), 200, {'ContentType':'application/json'}
        except:
            return json.dumps(ordered), 200, {'ContentType':'application/json'}
    except Exception as oops:
        print(oops)
        return str(oops), 500, {'ContentType':'application/json'}


@app.route('/bound', methods=['POST'])
def bound():
    global data
    try:
        results = list()
        payload = request.json
        payload = dejsonify(payload)
        field = payload['field']
        lower_bound = payload['lower_bound']
        upper_bound = payload['upper_bound']
        for i in self.data:
            try:
                if i[field] >= lower_bound and i[field] <= upper_bound:
                    results.append(i)
            except:
                continue
        results = jsonify(results)
        return json.dumps(results), 200, {'ContentType':'application/json'}
    except Exception as oops:
        print(oops)
        return str(oops), 500, {'ContentType':'application/json'}


@app.route('/save', methods=['POST'])
def save():
    global data
    try:
        with open('nexus.pickle', 'wb') as outfile:
            pickle.dump(data, outfile)
        return 'successfully saved data', 200, {'ContentType':'application/json'}
    except Exception as oops:
        print(oops)
        return str(oops), 500, {'ContentType':'application/json'}


if __name__ == '__main__':
    try:
        data = load()
    except Exception as oops:
        print(oops)
        data = list()
    app.run(host='0.0.0.0', port=8888)