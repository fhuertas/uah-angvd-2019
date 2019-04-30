import random
import time

from confluent_kafka import Producer


def producer():
    p = Producer({'bootstrap.servers': 'localhost:9092'})

    def delivery_report(err, msg):
        if err is not None:
            print('Error: {}'.format(err))
        else:
            print('Deilvered to: {}'.format(msg.topic()))

    while True:
        p.poll(0)

        data = str(random.randint(-10, 40)) + ',' + "{:.6f}".format(random.uniform(-40.0, 40.0)) \
                   + ',' + "{:.6f}".format(random.uniform(-40.0, 40.0))

        time.sleep(random.uniform(0.5, 3.0))

        p.produce('topic_ej1', data.encode('utf-8'), callback=delivery_report)


producer()
