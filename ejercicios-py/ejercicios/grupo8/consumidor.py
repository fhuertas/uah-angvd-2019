import time

from confluent_kafka import Consumer

c = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': round(time.time() * 1000),
    'auto.offset.reset': 'earliest'
})
c.subscribe(['this-is-a-topic'])
while True:
    msg = c.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue
    print('T, latitud, longitud: ', msg.value())

c.close()
