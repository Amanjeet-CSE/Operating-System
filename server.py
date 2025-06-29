from flask import Flask, send_from_directory, jsonify
import json

app = Flask(__name__, static_folder="public")

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@app.route('/metrics')
def metrics():
    with open("data.json") as f:
        return jsonify(json.load(f))

if __name__ == '__main__':
    app.run(port=8080, debug=True)
