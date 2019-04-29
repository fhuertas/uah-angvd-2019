import time

from confluent_kafka import Consumer


def consumidor():
    c = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': round(time.time() * 1000),
        'auto.offset.reset': 'earliest'
    })
    c.subscribe(['topic'])
    while True:
        mensaje = c.poll(1.0)
        if mensaje is None:
            continue
        if mensaje.error():
            print("Consumer error: {}".format(mensaje.error()))
            continue
        mensaje = mensaje.value().decode('utf-8').split(',')
        print('Temperatura:' + mensaje[0] + 'location: {latitude:' + mensaje[1] + ', longitud' + mensaje[2])
    c.close()


consumidor()
