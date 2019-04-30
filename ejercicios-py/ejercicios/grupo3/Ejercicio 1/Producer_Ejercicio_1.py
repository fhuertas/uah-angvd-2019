import random
from confluent_kafka import Producer
import time


class Sensor(object):
    def __init__(self, temperature, latitude, longitude):
        self.lat = latitude
        self.long = longitude
        self.temp = temperature

    def get_reading_csv(self):
        return str(str(self.temp) + "," + str(self.long) + "," + str(self.lat))


def generate_data():

    # Will produce data indefinitely. Stop running to stop producing data.
    devices = []

    while True:

        temperature = random.randint(0, 40)
        latitude = random.uniform(15, 40)
        longitude = random.uniform(15, 40)

        devices.append(Sensor(temperature, latitude, longitude))

        for device in devices:
            reading = device.get_reading_csv()
            yield reading

        time.sleep(4.0)


def producer_example():

    topic = "sensorsTemperature"

    p = Producer({'bootstrap.servers': 'localhost:9092'})

    def delivery_report(err, msg):
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} {}'.format(msg.topic(), msg.value()))

    for reading in generate_data():
        p.poll(0)
        p.produce(topic, value=reading.encode('utf-8'), callback=delivery_report)

    p.flush()


if __name__ == "__main__":
    producer_example()
