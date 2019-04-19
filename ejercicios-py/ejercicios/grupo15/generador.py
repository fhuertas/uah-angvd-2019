from confluent_kafka import Producer
import numpy as np

def generador_aleatorios():
    num = int(np.random.randint(1,1999, size = 1))
    return num


def productor():
    p = Producer({'bootstrap.servers': "localhost:19092,localhost:29092,localhost:39092"})

    def delivery_report(err, msg):
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))
    try:
        for val in range(1, 100000):
            temp = generador_aleatorios()
            p.produce('tnumeros',str(temp).encode('utf-8'), callback=delivery_report)
            p.poll(2)

    except KeyboardInterrupt:
        pass

    p.flush()


if __name__ == "__main__":
    productor()
