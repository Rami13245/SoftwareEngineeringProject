from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib, json, os

app = Flask(__name__)
CORS(app)

# Load your trained model
model = joblib.load('random_forest_model.pkl')

# Define possible interests (based on your dataset)
all_interests = ['Nature', 'Food', 'Adventure', 'History', 'Nightlife', 'Shopping', 'Beaches']

# Mapping functions
budget_map = {'low': 0, 'medium': 1, 'high': 2}
type_map = {'solo': 0, 'family': 1, 'group': 2}

# Duration mapping (to convert duration ranges into numeric values)
duration_mapping = {
    '1-2 days': 1.5,
    '3-5 days': 4,
    '6-9 days': 7.5,
    '10+ days': 12
}

@app.route('/')
def index():
    return "TripTastic API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    # Extract data from the request
    interests = data['interests']  # List of interests (example: ['Food', 'Adventure'])
    budget = data['budget'].lower()  # Example: 'low'
    duration = data['duration']      # Example: '6-7 days'
    trip_type = data['type'].lower() # Example: 'solo'

    print("Received:", interests, budget, duration, trip_type)

    # One-hot encode interests: 7 features for each possible interest
    interest_vector = [1 if interest in interests else 0 for interest in all_interests]

    # Map budget: 1 feature
    budget_value = budget_map.get(budget, 0)

    # Map duration: 1 feature
    duration_value = duration_mapping.get(duration, 0)

    # Map trip type: 4 features (one-hot encoding for solo, family, group)
    type_vector = [
        1 if trip_type == 'solo' else 0,
        1 if trip_type == 'family' else 0,
        1 if trip_type == 'group' else 0,
        1 if trip_type == 'couple' else 0  # Added 'couple' as a possible trip type
    ]

    # Combine all features into one input vector (13 features)
    input_vector = interest_vector + [budget_value, duration_value] + type_vector

    # Predict
    probabilities = model.predict_proba([input_vector])[0]
    top_indices = probabilities.argsort()[-3:][::-1]
    top_recommendations = [model.classes_[i] for i in top_indices]

    return jsonify({'recommended_trips': top_recommendations})

if __name__ == '__main__':
    app.run(debug=True)






user_file = 'users.json'

def read_users():
    if os.path.exists(user_file):
        with open(user_file, 'r') as f:
            return json.load(f)
    return {}

def write_users(data):
    with open(user_file, 'w') as f:
        json.dump(data, f)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    users = read_users()
    if data['email'] in users:
        return jsonify({'message': 'User already exists'}), 400
    users[data['email']] = data
    write_users(users)
    return jsonify({'message': 'User created successfully'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    users = read_users()
    user = users.get(data['email'])
    if user and user['password'] == data['password']:
        return jsonify({'message': 'Login successful'})
    return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(debug=True)
