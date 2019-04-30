import json
from time import time, sleep

import numpy as np
from confluent_kafka import Producer

p = Producer({'bootstrap.servers': 'localhost:9092'})


def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))


def generador():
    lista = []
    T = int(np.random.random_integers(low=-30, high=40))
    Lat = float(np.random.uniform(low=-90.0, high=90.0))
    Long = float(np.random.uniform(low=-180.0, high=180.0))
    lista.append(T)
    lista.append(Lat)
    lista.append(Long)
    return lista


while True:
    startTime = time()
    generador()
    endTime = time() - startTime
    sleep(1.0 - endTime)
    numeros = []
    numeros = generador()
    for numero in numeros:
        p.poll(1.0)
    p.produce('this-is-a-topic', value=json.dumps(numeros).encode('UTF-8'))
    print(json.dumps(numeros).encode('UTF-8'))
    # p.produce('this-is-a-topic',str(numeros.value().decode('utf-8')))
    p.flush(1.0)
