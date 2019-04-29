from confluent_kafka import Producer
import random
import time
def productor():
    p = Producer({'bootstrap.servers': 'localhost:9092'})

    def delivery_report(err, msg):
        """ Called once for each message produced to indicate delivery result.Triggered by poll() or flush(). """
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Messagedelivered to {} [{}]'.format(msg.topic(), msg.partition()))

    while True:
        # Trigger any available delivery report callbacks from previous produce() calls
        p.poll(0)
        nums = str(random.randint(-10, 40)) + ',' + "{:.6f}".format(random.uniform(-40.0, 40.0)) \
               + ',' + "{:.6f}".format(random.uniform(-40.0, 40.0))
        # Asynchronously produce a message, the delivery report callback
        # will be triggered from poll() above, or flush() below, when the message has
        # been successfully delivered or failed permanently.
        time.sleep(1)
        p.produce('topic', nums.encode('utf-8'), callback=delivery_report)
        # Wait for any outstanding messages to be delivered and delivery report
        # callbacks to be triggered.
        p.flush()


productor()
