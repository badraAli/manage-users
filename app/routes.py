from flask import abort, request, jsonify, render_template
from .models import User
from . import db

def init_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/users', methods=['GET'])
    def get_users():
        users = User.query.all()
        return jsonify([{'id': user.id, 'username': user.username, 'email': user.email} for user in users])
    
    @app.route('/users/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        user = db.session.get(User, user_id)
        if user is None:
            abort(404)  # Renvoie une erreur 404 si l'utilisateur n'existe pas
        return jsonify({'id': user.id, 'username': user.username, 'email': user.email})

    @app.route('/users', methods=['POST'])
    def create_user():
        data = request.get_json()
        new_user = User(username=data['username'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'id': new_user.id, 'username': new_user.username, 'email': new_user.email}), 201

    @app.route('/users/<int:user_id>', methods=['PUT'])
    def update_user(user_id):
        user = db.session.get(User, user_id)
        if user is None:
            abort(404)  # Renvoie une erreur 404 si l'utilisateur n'existe pas
        data = request.get_json()
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        db.session.commit()
        return jsonify({'id': user.id, 'username': user.username, 'email': user.email})

    @app.route('/users/<int:user_id>', methods=['DELETE'])
    def delete_user(user_id):
        user = db.session.get(User, user_id)
        if user is None:
            abort(404)  # Renvoie une erreur 404 si l'utilisateur n'existe pas
        db.session.delete(user)
        db.session.commit()
        return '', 204