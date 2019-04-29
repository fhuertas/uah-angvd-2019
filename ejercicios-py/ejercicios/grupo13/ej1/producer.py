import time

import numpy as np
from confluent_kafka import Producer


def genera_lectura():
    '''This function generates a sample of temperature, latitude and longitude'''

    temp = np.random.randint(-5, 50)

    latitud = np.round(3 + np.random.random(), decimals=6)
    longitud = np.round(40 + np.random.random(), decimals=6)

    linea = str(temp) + ',' + str(latitud) + ',' + str(longitud)
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
        p.produce('this-is-a-topic', genera_lectura().encode('utf-8'), callback=delivery_report)

        tiempoDormir = 0.5 + np.random.random()
        time.sleep(tiempoDormir)
    # Wait for any outstanding messages to be delivered and delivery report
    # callbacks to be triggered.

    p.flush()


if __name__ == "__main__":
    main()
