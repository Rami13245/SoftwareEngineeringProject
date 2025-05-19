# Admin login credentials (for demo purposes)
ADMIN_EMAIL = 'admin@triptastic.com'
ADMIN_PASS = 'admin123'

@app.route('/admin-login', methods=['POST'])
def admin_login():
    data = request.get_json()
    if data['email'] == ADMIN_EMAIL and data['password'] == ADMIN_PASS:
        return jsonify({'message': 'Admin login successful'})
    return jsonify({'message': 'Access denied'}), 403

@app.route('/users', methods=['GET'])
def get_users():
    users = read_users()
    user_list = [{'name': v['name'], 'email': k, 'age': v['age']} for k, v in users.items()]
    return jsonify({'users': user_list})

@app.route('/delete-user', methods=['POST'])
def delete_user():
    data = request.get_json()
    users = read_users()
    if data['email'] in users:
        del users[data['email']]
        write_users(users)
        return jsonify({'message': 'User deleted'})
    return jsonify({'message': 'User not found'}), 404
