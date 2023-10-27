from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import joblib
import os
import csv

dt = joblib.load("./static/final.joblib")

app = Flask(__name__)
CORS(app)

@app.route("/hola", methods=["GET"])
def inicio():
    return "Hola Mundo"

@app.route("/predict_json", methods=["POST"])
def predict_json():
    data = request.json
    X = [[
        float(data["pH"]),
        float(data["sulphates"]),
        float(data["alcohol"])
        ]]
    y_pred = dt.predict(X)
    return jsonify({"result": y_pred[0]})


@app.route("/predict_form", methods=["POST"])
def predict_form():
    data = request.form
    X = [[
        float(data["pH"]),
        float(data["sulphates"]),
        float(data["alcohol"])
        ]]
    y_pred = dt.predict(X)
    return jsonify({"result": y_pred[0]})

@app.route("/predict_file", methods=["POST"])
def predict_file():
    files = request.files["archivo"]
    filename = secure_filename(file.filename)
    # file.save(f"./static/{filename}")
    path = file.save(os.path.join(os.getcwd(), "static", filename))
    file.save(path)
    with open(path, "f") as f:
        f.readline()
        reader = csv.reader(f)
        # X = []
        # for row in reader:
        X = [float(row[0]), float(row[1]), float(row[2])]
        y_pred = dt.predict(X)
        return jsonify({
            "results": [{key: f"{k}",
                         "results": f"{v}"} for k, v in enumerate(y_pred)]
        })


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=8081)