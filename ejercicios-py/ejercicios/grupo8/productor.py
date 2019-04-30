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


def generador_valor():
    lista = []
    temperatura = int(np.random.random_integers(-50, 80))
    latitud = float(np.random.uniform(low=-90.0, high=90.0))
    longitud = float(np.random.uniform(low=-180.0, high=180.0))
    lista.append(temperatura)
    lista.append(latitud)
    lista.append(longitud)
    return lista


while True:
    startTime = time()
    generador_valor()
    endTime = time() - startTime
    sleep(1.0 - endTime)
    valores = []
    valores = generador_valor()
    for valor in valores:
        p.poll(1.0)
        p.produce('this-is-a-topic', value=json.dumps(valores).encode('UTF-8'))
        print(json.dumps(valores).encode('UTF-8'))
        # p.produce('this-is-a-topic',str(valores.value().decode('utf-8')))
    p.flush(1.0)
