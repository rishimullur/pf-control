from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for health details
health_details = {}

# In-memory storage for dietary data
dietary_data = {}

@app.route('/save_health_details', methods=['POST'])
def save_health_details():
    data = request.get_json()
    if data:
        user_id = data.get('user_id')
        health_details[user_id] = data
        return jsonify({'message': 'Health details saved successfully'}), 200
    else:
        return jsonify({'error': 'No data provided'}), 400

@app.route('/get_health_details/<user_id>', methods=['GET'])
def get_health_details(user_id):
    if user_id in health_details:
        return jsonify(health_details[user_id]), 200
    else:
        return jsonify({'error': 'Health details not found'}), 404

@app.route('/receive_dietary_data', methods=['POST'])
def receive_dietary_data():
    data = request.get_json()
    if data:
        user_id = data.get('user_id')
        dietary_data[user_id] = data
        return jsonify({'message': 'Dietary data received successfully'}), 200
    else:
        return jsonify({'error': 'No data provided'}), 400

if __name__ == '__main__':
    app.run(debug=True)