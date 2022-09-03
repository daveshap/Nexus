import requests
from time import time


def send(payload):
    url = 'http://127.0.0.1:8888/add'
    response = requests.request(method='POST', url=url, json=payload)
    print(response.text)


def search(payload):
    url = 'http://127.0.0.1:8888/search'
    response = requests.request(method='POST', url=url, json=payload)
    return response.json()


if __name__ == '__main__':
    info = {'content': 'bacon', 'microservice': 'test', 'model': 'there is no spoon', 'type': 'test'}
    for n in range(0, 50):
        start = time()
        send(info)
        print(time() - start)