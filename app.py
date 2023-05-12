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
prediction_duration_seconds = Histogram(
    "prediction_duration_seconds", "Prediction duration seconds"
)
prediction_duration_summary = Summary(
    "prediction_duration_summary", "Prediction duration summary"
)


@prediction_duration_seconds.time()
@prediction_duration_summary.time()
@app.route("/", methods=["GET", "POST"])
def index():
    global total_predictions, correct_predictions
    if request.method == "POST":
        review = request.form["review"]
        payload = {"msg": review}
        response = requests.post(f"{model_service_url}/", json=payload)
        data = response.json()
        total_predictions.inc()
        return jsonify(data)

    return render_template("index.html")


@app.route("/correctness", methods=["POST"])
def correctness():
    user_feedback = request.json.get("correct", False)
    if user_feedback:
        correct_predictions.inc()
    prediction_accuracy.set(
        correct_predictions._value / total_predictions._value
        if total_predictions._value
        else 0
    )
    return jsonify({"status": "success"})


app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {"/metrics": make_wsgi_app()})
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
