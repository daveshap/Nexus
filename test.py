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
    url = 'http://127.0.0.1:8888/add'
    response = requests.request(method='POST', url=url, json=payload)
    return response.json()
    


if __name__ == '__main__':
    print('instantiating arrays')
    dimension = 512
    count = 500
    np.random.seed(1)             
    print('loading up the database')
    for n in range(0, count):
        vector = np.random.random(dimension).astype('float16')
        info = {'vector': str(vector), 'time': str(time()), 'uuid': str(uuid4())}
        send(info)
        print(n)
        exit()
    info = {'vector': np.array2string(np.random.random(dimension).astype('float16')), 'field': 'vector', 'count': 5}
    results = search(info)
    pprint(results)