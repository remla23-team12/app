from flask import Flask, render_template, request, jsonify
from prometheus_client import Counter, Gauge, Histogram, Summary, make_wsgi_app
import requests
import os
from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = Flask(__name__)
model_service_url = os.environ.get("MODEL_SERVICE_URL", "http://localhost:8080")

total_predictions = Counter("total_predictions", "Total Predictions")
correct_predictions = Counter("correct_predictions", "Correct Predictions")
prediction_accuracy = Gauge("prediction_accuracy", "Prediction Accuracy")
prediction_accuracy_changes = Histogram(
    "prediction_accuracy_changes", "prediction_accuracy_changes"
)
prediction_duration_summary = Summary(
    "prediction_duration_summary", "Prediction duration counts and seconds summary"
)


@app.route("/", methods=["GET", "POST"])
def index():
    global total_predictions, correct_predictions
    if request.method == "POST":
        review = request.form["review"]
        payload = {"msg": review}
        response = make_prediction(payload)
        data = response.json()
        total_predictions.inc()
        return jsonify(data)

    return render_template("index.html")


@prediction_duration_summary.time()
def make_prediction(payload):
    # Here you make your prediction
    response = requests.post(f"{model_service_url}/", json=payload)
    return response


@app.route("/correctness", methods=["POST"])
def correctness():
    user_feedback = request.json.get("correct", False)
    if user_feedback:
        correct_predictions.inc()
    # if not this way TypeError: unsupported operand type(s) for /: mutex and mutex
    correct_predictions_value = int(correct_predictions._value._value)
    total_predictions_value = int(total_predictions._value._value)
    prediction_accuracy.set(
        correct_predictions_value / total_predictions_value
        if total_predictions_value
        else 0
    )
    prediction_accuracy_changes.observe(
        correct_predictions_value / total_predictions_value
    )
    return jsonify({"status": "success"})


app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {"/metrics": make_wsgi_app()})
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
