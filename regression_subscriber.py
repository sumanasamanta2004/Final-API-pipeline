from confluent_kafka import Consumer
import json
import joblib

# Load the regression model
model = joblib.load("iris_regression_model.pkl")

# Kafka consumer config
config = {
    'bootstrap.servers': 'localhost:52478',  # Use your correct Kafka port
    'group.id': 'regression_group',
    'auto.offset.reset': 'latest'
}

# Create Kafka Consumer instance
consumer = Consumer(config)
topic = "manage"
consumer.subscribe([topic])

print("✅ Regression Subscriber (using 3 features) listening to topic:", topic)

try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            print("⏳ Waiting for message...")
            continue

        if msg.error():
            print("❌ Kafka Error:", msg.error())
            continue

        # Parse JSON message from Kafka
        data = json.loads(msg.value().decode("utf-8"))
        print("📩 Received message:", data)

        # Use only 3 features
        features = [
            data["sepal_length"],
            data["sepal_width"],
            data["petal_length"]
        ]

        # Predict using the regression model
        prediction = model.predict([features])[0]

        print("🔍 Regression Prediction:")
        print(f"  → Predicted Value: {prediction:.4f}")

except KeyboardInterrupt:
    print("\n🛑 Stopped by user.")
finally:
    consumer.close()
