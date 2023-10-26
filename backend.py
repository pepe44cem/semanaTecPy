from flask import Flask, request
from flask_cors import CORS
import joblib

app = Flask(_name_)

@app.route("/hola", methods=["GET"])
def inicio():
    return "Hola mundo"

if _name_ == "_main_":
    app.run(host="0.0.0.0", debug=False, port=8081)