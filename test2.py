import requests


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
    for n in range(0, 50):
        info = {'vector': [0,1], 'content': 'bacon', 'microservice': 'test'}
        send(info)