from confluent_kafka import Producer
import numpy as np
import time

def generador_sondas():
    tem = int(np.random.randint(20,40, size = 1))
    lat = round(np.random.uniform(-90,90),4)
    lon = round(np.random.uniform(-180,180),6)
    msj = "{"+'"temperatura":{}'.format(tem)+","+'"location":{'+'"latitud":{}, "longitud":{}'.format(lat,lon)+ "}}"
    return msj


def producer_sondas():
    p = Producer({'bootstrap.servers': 'localhost:9092'})

    def delivery_report(err, msg):
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

    try:
        for val in range(1, 1000000):
            temp = generador_sondas()
            p.produce('this-is-a-topic',str(temp).encode('utf-8'), callback=delivery_report)
            time.sleep(1)

            # p.poll(1)

    except KeyboardInterrupt:
        pass

    p.flush()


if __name__ == "__main__":
    producer_sondas()
