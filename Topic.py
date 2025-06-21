from confluent_kafka import Producer
import json
import time

def delivery_report(err, msg):
    """ Called once for each message to indicate delivery result. """
    if err is not None:
        print(f"❌ Message delivery failed: {err}")
    else:
        print(f"✅ Message delivered to {msg.topic()} [{msg.partition()}]")

if __name__ == "__main__":
    config = {
        'bootstrap.servers': 'localhost:52478',  # 👈 Use the port shown under "Plaintext Ports"
        'acks': 'all'
    }

    producer = Producer(config)
    topic = "manage"

    # Sample message (can be any JSON/dict)
    message = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }

    # Convert dict to JSON string before sending
    producer.produce(
        topic=topic,
        key="iris_sample",
        value=json.dumps(message),
        callback=delivery_report
    )

    # Wait for delivery
    producer.poll(1)
    producer.flush()
