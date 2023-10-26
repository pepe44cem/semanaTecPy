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
    return "Hola mundo"

@app.route("/predict_json", method = ["POST"])
def predict_json():
    data = request.json
    x = [[
        float(data["pH"]),
        float(data["sulphates"]),
        float(data["alcohol"])
        ]]
    
    y_pred = dt.predict(x)
    print(y_pred)
    return jsonify({"result": y_pred[0]})

@app.route("/predict_form", method = ["POST"])
def predict_form():
    data = request.form
    x = [[
        float(data["pH"]),
        float(data["sulphates"]),
        float(data["alcohol"])
        ]]
    
    y_pred = dt.predict(x)
    print(y_pred)
    return jsonify({"result": y_pred[0]})

@app.route("/predict_file", method = ["POST"])
def predict_file():
    file = request.file["archivo"]
    filename = secure_filename(file)
    #file.save(f"./static/{filename}")
    path = os.path(os.getcwd(), "static", filename)
    file.save(path)
    with open(path, "r") as f:
        f.readline()
        reader = csv.reader
        x = [[float(row[0]), float(row[1]), float(row[2])] for row in reader]
        y_pred = dt.predict(x)
        return jsonify({
            "result" : [{"key" : f"{k}",
                         "result" : f"{v}"} for k, v in enumerate(y_pred)]
        })
        
    

    

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=8081)