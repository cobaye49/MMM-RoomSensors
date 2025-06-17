from flask import Flask, jsonify
from sensor import read_sensor

app = Flask(__name__)

@app.route("/sensor")
def get_sensor_data():
    return jsonify(read_sensor())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)