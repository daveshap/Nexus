import requests
from time import time
from uuid import uuid4
import numpy as np


def send(payload):
    url = 'http://127.0.0.1:8888/add'
    response = requests.request(method='POST', url=url, json=payload)
    print(response.text)


if __name__ == '__main__':
    print('instantiating arrays')
    dimension = 512
    count = 10000000
    np.random.seed(1)             
    print('loading up the database')
    for n in range(0, count):
        vector = np.random.random(dimension).astype('float16')
        info = {'vector': str(vector), 'time': str(time()), 'uuid': str(uuid4())}
        send(info)
        if n % 50000 == 0:
            print(n)
        #exit()