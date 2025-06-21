from confluent_kafka import Consumer
import json
import joblib

# Load classification model & preprocessing tools
model = joblib.load("iris_logistic_model.pkl")
scaler = joblib.load("iris_scaler.pkl")
label_encoder = joblib.load("iris_label_encoder.pkl")

# Kafka config
config = {
    'bootstrap.servers': 'localhost:52478',
    'group.id': 'classification_group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(config)
topic = "manage"
consumer.subscribe([topic])

print("✅ Classification Subscriber listening on topic:", topic)

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print("❌ Error:", msg.error())
            continue

        data = json.loads(msg.value().decode('utf-8'))

        features = [
            data["sepal_length"],
            data["sepal_width"],
            data["petal_length"],
            data["petal_width"]
        ]

        scaled = scaler.transform([features])
        prediction_index = model.predict(scaled)[0]
        prediction_label = label_encoder.inverse_transform([prediction_index])[0]

        print("🔍 Classification Result:")
        print(f"  → Class Index: {prediction_index}")
        print(f"  → Class Label: {prediction_label}")
except KeyboardInterrupt:
    pass
finally:
    consumer.close()
