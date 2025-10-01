# app/routes/auth_routes.py
from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from app.db import SessionLocal
from app.models import User
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    session = SessionLocal()
    try:
        password_hash = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()).decode()
        user = User(
            emailid=data['emailid'],
            username=data['username'],
            firstname=data['firstname'],
            lastname=data['lastname'],
            age=int(data['age']),
            gender=data['gender'],
            industry=data['industry'],
            profession=data['profession'],
            password_hash=password_hash
        )
        session.add(user)
        session.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except IntegrityError:
        session.rollback()
        return jsonify({'error': 'Email or username already exists'}), 400
    finally:
        session.close()

@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    session = SessionLocal()
    user = session.query(User).filter_by(emailid=data['emailid']).first()
    session.close()
    if user and bcrypt.checkpw(data['password'].encode(), user.password_hash.encode()):
        return jsonify({'user_id': user.user_id, 'username': user.username}), 200
    return jsonify({'error': 'Invalid credentials'}), 401
