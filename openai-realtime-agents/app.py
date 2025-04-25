# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/python/process', methods=['POST'])
def process_data():
    data = request.json
    # Custom Python logic here
    result = {"processed": True, "input": data, "result": "Processed by Python"}
    return jsonify(result)

@app.route('/api/python/analyze', methods=['POST'])
def analyze_data():
    data = request.json
    # Custom data analysis with Python libraries
    # Example: Using pandas, numpy, scikit-learn, etc.
    result = {"analyzed": True, "input": data, "analysis": "Data analyzed by Python"}
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)