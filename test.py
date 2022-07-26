import requests
from time import time
from uuid import uuid4
import numpy as np
from pprint import pprint


def send(payload):
    url = 'http://127.0.0.1:8888/add'
    response = requests.request(method='POST', url=url, json=payload)
    print(response.text)


def search(payload):
    url = 'http://127.0.0.1:8888/search'
    response = requests.request(method='POST', url=url, json=payload)
    return response.json()


def save():
    url = 'http://127.0.0.1:8888/save'
    response = requests.request(method='POST', url=url)
    print(response.text)
    
    


if __name__ == '__main__':
    dimension = 1024
    count = 5000
    count = 0
    np.random.seed(1)             
    print('loading up the database')
    for n in range(0, count):
        vector = list(np.random.random(dimension).astype('float16'))
        info = {'vector': str(vector), 'time': time(), 'uuid': str(uuid4())}
        start = time()
        send(info)
        end = time()
        print(n, end - start)
    save()
    vector = list(np.random.random(dimension).astype('float16'))
    info = {'vector': str(vector), 'field': 'vector', 'count': 5}
    start = time()
    results = search(info)
    end = time()
    print(len(results), 'fetched in', end - start, 'seconds')