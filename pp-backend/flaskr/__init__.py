from flask import Flask, jsonify, request
from flask_cors import CORS
from main import invoke

app = Flask(__name__)
CORS(app)

@app.route('/hello', methods=['POST'])
def hello():
    query = request.json['data']  # Adjusted to support both form and JSON
    data = {
        'message': invoke(query),
        'query': query  # Echoing back the query
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=5000, debug=True)