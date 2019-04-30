import time

import numpy as np
from confluent_kafka import Producer


def crearDatos():
    '''This function generates a sample of temperature, latitude and longitude'''

    tmp = np.random.randint(-15, 44)
    long = np.round(-180 + 360 * np.random.random(), decimals=6)
    lat = np.round(-90 + 180 * np.random.random(), decimals=6)

    linea = str(tmp) + ',' + str(lat) + ',' + str(long)
    print(linea)
    return linea


def main():
    p = Producer({'bootstrap.servers': 'localhost:9092'})

    def delivery_report(err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

    # for data in some_data_source:
    while True:
        # Trigger any available delivery report callbacks from previous produce() calls
        p.poll(0)

        # Asynchronously produce a message, the delivery report callback
        # will be triggered from poll() above, or flush() below, when the message has
        # been successfully delivered or failed permanently.
        p.produce('topic', crearDatos().encode('utf-8'), callback=delivery_report)

        sleepTime = 0.7 + 0.6 * np.random.random()
        # print(sleepTime)
        time.sleep(sleepTime)
    # Wait for any outstanding messages to be delivered and delivery report
    # callbacks to be triggered.

    p.flush()


if __name__ == "__main__":
    main()
