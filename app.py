from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mydatabase'
mongo = PyMongo(app)

@app.route('/users', methods=['GET'])
def get_all_users():
    users = mongo.db.users.find()
    result = []
    for user in users:
        result.append({
            'id': str(user['_id']),
            'name': user['name'],
            'email': user['email'],
            'password': user['password']
        })
    return jsonify(result)

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    if user:
        result = {
            'id': str(user['_id']),
            'name': user['name'],
            'email': user['email'],
            'password': user['password']
        }
        return jsonify(result)
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/users', methods=['POST'])
def create_user():
    user = {
        'name': request.json['name'],
        'email': request.json['email'],
        'password': request.json['password']
    }
    result = mongo.db.users.insert_one(user)
    return jsonify(str(result.inserted_id))

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    if user:
        mongo.db.users.update_one({'_id': ObjectId(id)}, {'$set': {
            'name': request.json['name'],
            'email': request.json['email'],
            'password': request.json['password']
        }})
        return jsonify({'message': 'User updated successfully'})
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    if user:
        mongo.db.users.delete_one({'_id': ObjectId(id)})
        return jsonify({'message': 'User deleted successfully'})
    else:
        return jsonify({'error': 'User not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
