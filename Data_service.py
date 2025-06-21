from flask import Flask, request, jsonify
import joblib

# Load model, scaler, and label encoder
model = joblib.load("iris_logistic_model.pkl")
scaler = joblib.load("iris_scaler.pkl")
label_encoder = joblib.load("iris_label_encoder.pkl")

app = Flask(__name__)

# Define expected input range for validation (based on Iris dataset)
VALID_RANGES = {
    "sepal_length": (4.0, 8.0),
    "sepal_width": (2.0, 4.5),
    "petal_length": (1.0, 7.0),
    "petal_width": (0.1, 2.5)
}

def validate_input(data):
    errors = {}
    for feature, (min_val, max_val) in VALID_RANGES.items():
        value = data.get(feature)
        if value is None:
            errors[feature] = "Missing value"
        elif not isinstance(value, (int, float)):
            errors[feature] = f"Invalid type. Expected number, got {type(value).__name__}"
        elif not (min_val <= float(value) <= max_val):
            errors[feature] = f"Out of valid range ({min_val} - {max_val})"
    return errors

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        # ✅ Validate input
        validation_errors = validate_input(data)
        if validation_errors:
            return jsonify({"validation_errors": validation_errors}), 400

        features = [
            float(data["sepal_length"]),
            float(data["sepal_width"]),
            float(data["petal_length"]),
            float(data["petal_width"])
        ]

        scaled = scaler.transform([features])
        prediction_index = model.predict(scaled)[0]
        prediction_label = label_encoder.inverse_transform([prediction_index])[0]

        return jsonify({
            "predicted_class_index": int(prediction_index),
            "predicted_class_label": prediction_label
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    port = 5001
    print(f"✅ Server running at http://127.0.0.1:{port}/predict")
    app.run(debug=True, port=port)
