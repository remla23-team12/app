from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)
model_service_url = os.environ.get("MODEL_SERVICE_URL", "http://localhost:8080")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        review = request.form["review"]
        payload = {"msg": review}
        response = requests.post(f"{model_service_url}/", json=payload)
        data = response.json()
        return jsonify(data)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
