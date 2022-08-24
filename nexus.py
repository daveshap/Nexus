import flask
import json
from flask import request
import os
import logging
import numpy as np
import pickle


nexus_port = int(os.getenv('NEXUS_PORT', 8888))


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app = flask.Flask('nexus')


def load(filepath='nexus.pickle'):
    with open(filepath, 'rb') as infile:
        data = pickle.load(infile)
    return data


def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


@app.route('/add', methods=['POST'])
def add():  # REQUIRED: time, vector
    global data
    try:
        payload = request.json
        data.append(payload)
        print(payload['time'], payload['service'], payload['content'])
        filename = '%s_%s.txt' % (payload['time'], payload['service'])
        save_file('logs/%s' % filename, payload['content'])
        return 'successfully added record', 200, {'ContentType':'application/json'}
    except Exception as oops:
        print(oops)
        return str(oops), 500, {'ContentType':'application/json'}


@app.route('/search', methods=['POST'])
def search():  # REQUIRED: vector, count
    global data
    try:
        results = list()
        payload = request.json
        count = payload['count']
        vector = payload['vector']
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


@app.route('/fetch', methods=['POST'])
def fetch():  # REQUIRED: field, count, value, sortby, reverse
    global data
    try:
        results = list()
        payload = request.json
        field = payload['field']  # which field to search each record for
        value = payload['value']  # value of field to match
        reverse = payload['reverse']  # boolean True == descending order, False == ascending
        sortby = payload['sortby']  # which field to sort by (such as time)
        count = payload['count']  # total number to return
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


@app.route('/bound', methods=['POST'])
def bound():
    global data
    try:
        results = list()
        payload = request.json
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
    app.run(host='0.0.0.0', port=nexus_port)
