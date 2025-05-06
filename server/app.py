from flask import Flask, jsonify, request
from server.models import db
from server.controller import UserController

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://simple_user:2822928229@localhost/simple_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://simple_user:2822928229@localhost/simple_app?options=-csearch_path%3Dmyapp'


db.init_app(app)
# Создаем таблицы при запуске
with app.app_context():
    db.create_all()

@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    user = UserController.create_user(data)
    return jsonify(user.to_dict()), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = UserController.get_all_users()
    return jsonify([user.to_dict() for user in users])

if __name__ == '__main__':
    app.run(debug=True)