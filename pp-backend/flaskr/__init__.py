from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/hello', methods=['POST'])
def hello():
    query = request.form.get('query') or request.json.get('data')  # Adjusted to support both form and JSON
    print(query)
    data = {
        'message': 'yoooo',
        'query': query  # Echoing back the query
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
